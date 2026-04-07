import json
from pathlib import Path

import networkx as nx
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

DEFAULT_GRAPH_PATH = Path("graphify-out/graph.json")


def load_graph(graph_path: Path) -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    data = json.loads(graph_path.read_text(encoding="utf-8"))
    nodes = pd.DataFrame(data.get("nodes", []))
    links = pd.DataFrame(data.get("links", []))
    return nodes, links, data


def normalize_nodes(nodes: pd.DataFrame) -> pd.DataFrame:
    df = nodes.copy()
    for col in ["id", "label", "file_type", "source_file", "community"]:
        if col not in df.columns:
            df[col] = None
    df["label"] = df["label"].fillna("")
    df["source_file"] = df["source_file"].fillna("")
    df["file_type"] = df["file_type"].fillna("unknown")
    df["community"] = df["community"].fillna(-1).astype(int)
    df["is_paper"] = (df["file_type"].eq("paper") | df["source_file"].str.lower().str.endswith(".pdf"))
    return df


def normalize_links(links: pd.DataFrame) -> pd.DataFrame:
    df = links.copy()
    for col in ["source", "target", "relation", "confidence", "confidence_score", "source_file"]:
        if col not in df.columns:
            df[col] = None
    df["relation"] = df["relation"].fillna("unknown")
    df["confidence"] = df["confidence"].fillna("unknown")
    df["confidence_score"] = pd.to_numeric(df["confidence_score"], errors="coerce").fillna(0.0)
    df["source_file"] = df["source_file"].fillna("")
    return df


def compute_paper_scores(nodes: pd.DataFrame, links: pd.DataFrame) -> pd.DataFrame:
    paper_nodes = nodes[nodes["is_paper"]].copy()
    if paper_nodes.empty:
        return paper_nodes

    degree_counts = pd.concat([links["source"], links["target"]]).value_counts().rename("degree")
    inferred = links[links["confidence"].str.upper().eq("INFERRED")]
    inferred_counts = pd.concat([inferred["source"], inferred["target"]]).value_counts().rename("inferred_degree")

    paper_nodes = paper_nodes.merge(degree_counts, left_on="id", right_index=True, how="left")
    paper_nodes = paper_nodes.merge(inferred_counts, left_on="id", right_index=True, how="left")
    paper_nodes["degree"] = paper_nodes["degree"].fillna(0).astype(int)
    paper_nodes["inferred_degree"] = paper_nodes["inferred_degree"].fillna(0).astype(int)
    return paper_nodes.sort_values(["degree", "label"], ascending=[False, True])


def search_papers(papers: pd.DataFrame, query: str) -> pd.DataFrame:
    q = query.strip().lower()
    if not q:
        return papers

    tokens = [t for t in q.split() if t]

    def score_row(row: pd.Series) -> int:
        haystack = f"{row['label']} {row['source_file']}".lower()
        return sum(3 if t in row["label"].lower() else 1 for t in tokens if t in haystack)

    out = papers.copy()
    out["score"] = out.apply(score_row, axis=1)
    out = out[out["score"] > 0]
    return out.sort_values(["score", "degree", "label"], ascending=[False, False, True])


def build_plot(nodes: pd.DataFrame, links: pd.DataFrame, highlight_ids: set[str]) -> go.Figure:
    g = nx.Graph()

    for _, row in nodes.iterrows():
        g.add_node(
            row["id"],
            label=row["label"],
            community=row["community"],
            file_type=row["file_type"],
            source_file=row["source_file"],
        )

    for _, row in links.iterrows():
        src = row["source"]
        tgt = row["target"]
        if src in g and tgt in g:
            g.add_edge(src, tgt, relation=row["relation"], confidence=row["confidence"])

    if g.number_of_nodes() == 0:
        return go.Figure()

    pos = nx.spring_layout(g, seed=42, k=0.8 / max(1, g.number_of_nodes() ** 0.5), iterations=80)

    edge_x = []
    edge_y = []
    for u, v in g.edges():
        x0, y0 = pos[u]
        x1, y1 = pos[v]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    edge_trace = go.Scatter(
        x=edge_x,
        y=edge_y,
        line=dict(width=0.8, color="#9aa0a6"),
        hoverinfo="none",
        mode="lines",
    )

    node_x = []
    node_y = []
    node_text = []
    node_color = []
    node_size = []

    for nid, attrs in g.nodes(data=True):
        x, y = pos[nid]
        node_x.append(x)
        node_y.append(y)
        node_text.append(
            f"{attrs['label']}<br>Type: {attrs['file_type']}<br>Community: {attrs['community']}<br>Source: {attrs['source_file']}"
        )
        node_color.append(attrs["community"])
        node_size.append(24 if nid in highlight_ids else 14)

    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode="markers",
        hoverinfo="text",
        text=node_text,
        marker=dict(
            showscale=True,
            colorscale="Viridis",
            color=node_color,
            size=node_size,
            colorbar=dict(title="Community"),
            line=dict(width=1, color="#222"),
        ),
    )

    fig = go.Figure(data=[edge_trace, node_trace])
    fig.update_layout(
        title="Paper Relationship Graph",
        margin=dict(l=10, r=10, t=45, b=10),
        showlegend=False,
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        height=700,
    )
    return fig


def main() -> None:
    st.set_page_config(page_title="Paper Explorer", layout="wide")
    st.title("Paper Explorer")
    st.caption("Search papers and explore connections from graphify output")

    with st.sidebar:
        st.header("Settings")
        graph_path_input = st.text_input("Graph JSON path", str(DEFAULT_GRAPH_PATH))
        include_non_papers = st.checkbox("Include non-paper nodes in graph", value=False)

    graph_path = Path(graph_path_input)
    if not graph_path.exists():
        st.error(f"Graph file not found: {graph_path}")
        st.stop()

    try:
        nodes_raw, links_raw, _ = load_graph(graph_path)
    except Exception as exc:  # pragma: no cover
        st.exception(exc)
        st.stop()

    nodes = normalize_nodes(nodes_raw)
    links = normalize_links(links_raw)

    if nodes.empty:
        st.warning("No nodes found in graph data.")
        st.stop()

    papers = compute_paper_scores(nodes, links)
    total_papers = int(papers.shape[0])
    total_nodes = int(nodes.shape[0])
    total_edges = int(links.shape[0])

    c1, c2, c3 = st.columns(3)
    c1.metric("Papers", total_papers)
    c2.metric("Nodes", total_nodes)
    c3.metric("Edges", total_edges)

    with st.sidebar:
        communities = sorted(nodes["community"].dropna().unique().tolist())
        selected_communities = st.multiselect("Communities", communities, default=communities)
        relations = sorted(links["relation"].dropna().unique().tolist())
        selected_relations = st.multiselect("Relations", relations, default=relations)
        min_conf = st.slider("Min confidence score", 0.0, 1.0, 0.0, 0.05)

    query = st.text_input("Search papers (title/path keywords)")

    filtered_nodes = nodes[nodes["community"].isin(selected_communities)]
    filtered_links = links[
        links["relation"].isin(selected_relations)
        & (links["confidence_score"] >= min_conf)
        & links["source"].isin(filtered_nodes["id"])
        & links["target"].isin(filtered_nodes["id"])
    ]

    filtered_papers = papers[papers["community"].isin(selected_communities)]
    filtered_papers = search_papers(filtered_papers, query)

    if filtered_papers.empty:
        st.info("No papers matched your current filters.")
    else:
        st.subheader("Paper Results")
        display_cols = ["label", "source_file", "community", "degree", "inferred_degree"]
        if "score" in filtered_papers.columns:
            display_cols.insert(0, "score")
        st.dataframe(
            filtered_papers[display_cols],
            use_container_width=True,
            hide_index=True,
        )

    selected_paper = st.selectbox(
        "Inspect a paper",
        options=filtered_papers["id"].tolist() if not filtered_papers.empty else [],
        format_func=lambda nid: filtered_papers.set_index("id").loc[nid, "label"] if nid else "",
    )

    if selected_paper:
        st.subheader("Connections")
        local_edges = filtered_links[
            (filtered_links["source"] == selected_paper) | (filtered_links["target"] == selected_paper)
        ].copy()
        id_to_label = nodes.set_index("id")["label"].to_dict()
        local_edges["source_label"] = local_edges["source"].map(id_to_label)
        local_edges["target_label"] = local_edges["target"].map(id_to_label)
        st.dataframe(
            local_edges[["source_label", "relation", "target_label", "confidence", "confidence_score", "source_file"]],
            use_container_width=True,
            hide_index=True,
        )

    st.subheader("Graph View")
    graph_nodes = filtered_nodes if include_non_papers else filtered_nodes[filtered_nodes["is_paper"]]
    highlight_ids = set(filtered_papers["id"].head(8).tolist())
    fig = build_plot(graph_nodes, filtered_links, highlight_ids)
    st.plotly_chart(fig, use_container_width=True)


if __name__ == "__main__":
    main()
