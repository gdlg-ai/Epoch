import os
import requests
import gradio as gr

API_HOST = os.getenv("API_HOST", "api")
API_PORT = int(os.getenv("API_PORT", "8000"))
BASE = f"http://{API_HOST}:{API_PORT}"


def check_health():
    try:
        r = requests.get(f"{BASE}/health", timeout=5)
        return r.json()
    except Exception as e:
        return {"status": "error", "detail": str(e)}


def do_ingest(text, tags):
    tags_list = [t.strip() for t in tags.split(",") if t.strip()] if tags else []
    r = requests.post(f"{BASE}/ingest", json={"text": text, "tags": tags_list}, timeout=20)
    return r.json()


def do_query(q, k):
    r = requests.post(f"{BASE}/query", json={"query": q, "top_k": int(k)}, timeout=20)
    results = r.json().get("results", [])
    lines = [f"[{i+1}] ({x['score']:.3f}) {x['text']}  tags={x['tags']}" for i, x in enumerate(results)]
    return "\n".join(lines) if lines else "<no results>"


with gr.Blocks(title="Epoch PoC UI") as demo:
    gr.Markdown("""
    # Epoch — Minimal PoC UI
    Ingest short notes and query via a simple similarity search. First cut.
    """)

    with gr.Row():
        with gr.Column():
            gr.Markdown("## Health")
            btn_h = gr.Button("Check Health")
            out_h = gr.JSON(label="API Status")
            btn_h.click(fn=check_health, outputs=out_h)

        with gr.Column():
            gr.Markdown("## Ingest")
            in_text = gr.Textbox(label="Text", lines=4)
            in_tags = gr.Textbox(label="Tags (comma-separated)")
            btn_i = gr.Button("Ingest")
            out_i = gr.JSON(label="Result")
            btn_i.click(fn=do_ingest, inputs=[in_text, in_tags], outputs=out_i)

    gr.Markdown("## Query")
    q_text = gr.Textbox(label="Query", lines=2)
    q_k = gr.Slider(label="Top K", minimum=1, maximum=10, value=5, step=1)
    btn_q = gr.Button("Search")
    out_q = gr.Textbox(label="Results", lines=10)
    btn_q.click(fn=do_query, inputs=[q_text, q_k], outputs=out_q)

demo.queue()
demo.launch(server_name=os.getenv("UI_HOST", "0.0.0.0"), server_port=int(os.getenv("UI_PORT", "7860")))

