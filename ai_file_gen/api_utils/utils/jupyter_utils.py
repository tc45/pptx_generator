import nbformat as nbf
from nbconvert import HTMLExporter, NotebookExporter
from nbconvert.preprocessors import ExecutePreprocessor


def markdown_to_ipynb(md_content):
    nb = nbf.v4.new_notebook()
    cell = nbf.v4.new_markdown_cell(md_content)
    nb.cells.append(cell)
    return nb


def execute_notebook(nb):
    ep = ExecutePreprocessor()
    ep.preprocess(nb)

    html_exporter = HTMLExporter()
    html_data, _ = html_exporter.from_notebook_node(nb)

    # If you want to save notebook as .ipynb
    notebook_exporter = NotebookExporter()
    notebook_data, _ = notebook_exporter.from_notebook_node(nb)

    return html_data, notebook_data

