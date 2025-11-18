from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
import json
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import List

# ----- Paths -----
APP_DIR = Path(__file__).parent
SNIPPETS_FILE = APP_DIR / 'snippets.json'

# ----- Flask app with explicit templates/static paths -----
app = Flask(
    __name__,
    template_folder=os.path.join(APP_DIR, 'templates'),
    static_folder=os.path.join(APP_DIR, 'static')
)

# ----- OOP classes -----
@dataclass
class Snippet:
    id: int
    title: str
    description: str
    code: str  # CSS code

    def preview_style(self) -> str:
        """Return snippet's CSS for embedding into a <style> block."""
        return self.code

class SnippetManager:
    def __init__(self, storage_path: Path):
        self.storage_path = storage_path
        self.snippets: List[Snippet] = []
        self._load()

    def _load(self):
        if not self.storage_path.exists():
            self.snippets = []
            self._save()
            return
        with open(self.storage_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.snippets = [Snippet(**item) for item in data]

    def _save(self):
        with open(self.storage_path, 'w', encoding='utf-8') as f:
            json.dump([asdict(s) for s in self.snippets], f, indent=2)

    def all(self) -> List[Snippet]:
        return list(self.snippets)

    def add(self, title: str, description: str, code: str) -> Snippet:
        next_id = 1 if not self.snippets else max(s.id for s in self.snippets) + 1
        snippet = Snippet(id=next_id, title=title, description=description, code=code)
        self.snippets.append(snippet)
        self._save()
        return snippet

    def get(self, snippet_id: int) -> Snippet | None:
        for s in self.snippets:
            if s.id == snippet_id:
                return s
        return None

# ----- initialize manager -----
manager = SnippetManager(SNIPPETS_FILE)

# ----- routes -----
@app.route('/')
def index():
    snippets = manager.all()
    return render_template('index.html', snippets=snippets)

@app.route('/snippet/<int:snippet_id>')
def view_snippet(snippet_id):
    s = manager.get(snippet_id)
    if s is None:
        return redirect(url_for('index'))
    return render_template('view.html', snippet=s)

@app.route('/add', methods=['GET', 'POST'])
def add_snippet():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        code = request.form.get('code', '').strip()
        if title and code:
            manager.add(title=title, description=description, code=code)
            return redirect(url_for('index'))
    return render_template('add.html')

# Simple API for fetching snippets
@app.route('/api/snippets')
def api_snippets():
    return jsonify([asdict(s) for s in manager.all()])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)            self.snippets = [Snippet(**item) for item in data]

    def _save(self):
        with open(self.storage_path, 'w', encoding='utf-8') as f:
            json.dump([asdict(s) for s in self.snippets], f, indent=2)

    def all(self) -> List[Snippet]:
        return list(self.snippets)

    def add(self, title: str, description: str, code: str) -> Snippet:
        next_id = 1 if not self.snippets else max(s.id for s in self.snippets) + 1
        snippet = Snippet(id=next_id, title=title, description=description, code=code)
        self.snippets.append(snippet)
        self._save()
        return snippet

    def get(self, snippet_id: int) -> Snippet | None:
        for s in self.snippets:
            if s.id == snippet_id:
                return s
        return None

# ----- initialize manager -----
manager = SnippetManager(SNIPPETS_FILE)

# ----- routes -----
@app.route('/')
def index():
    snippets = manager.all()
    return render_template('index.html', snippets=snippets)

@app.route('/snippet/<int:snippet_id>')
def view_snippet(snippet_id):
    s = manager.get(snippet_id)
    if s is None:
        return redirect(url_for('index'))
    return render_template('view.html', snippet=s)

@app.route('/add', methods=['GET', 'POST'])
def add_snippet():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        code = request.form.get('code', '').strip()
        if title and code:
            manager.add(title=title, description=description, code=code)
            return redirect(url_for('index'))
    return render_template('add.html')

# Simple API for fetching snippets (used by client-side JS if desired)
@app.route('/api/snippets')
def api_snippets():
    return jsonify([asdict(s) for s in manager.all()])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
