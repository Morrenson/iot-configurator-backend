const api = '/models/';

async function loadList() {
    const r = await fetch(api);
    const m = await r.json();
    const l = document.getElementById('model-list');
    l.innerHTML = '';
    m.forEach(d => {
        const li = document.createElement('li');
        const a = document.createElement('a');
        a.textContent = d.name;
        a.href = `/view/${d.id}`;
        li.appendChild(a);
        l.appendChild(li);
    });
}

async function handleCreate(e) {
    e.preventDefault();
    const name = document.getElementById('name').value;
    const description = document.getElementById('description').value;
    let configuration;
    try { configuration = JSON.parse(document.getElementById('configuration').value); }
    catch { alert('Invalid JSON'); return; }
    const r = await fetch(api, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, description, configuration })
    });
    if (r.ok) window.location = '/';
    else alert('Error creating model');
}

async function loadDetail() {
    const id = window.location.pathname.split('/').pop();
    const r = await fetch(api + id);
    const d = await r.json();
    document.getElementById('model-detail').innerHTML = `
        <p><strong>ID:</strong> ${d.id}</p>
        <p><strong>Name:</strong> ${d.name}</p>
        <p><strong>Description:</strong> ${d.description || '(none)'}</p>
        <pre>${JSON.stringify(d.configuration, null, 2)}</pre>
    `;
}

document.addEventListener('DOMContentLoaded', () => {
    const p = window.location.pathname;
    if (p === '/' || p === '/index.html') loadList();
    else if (p === '/create') document.getElementById('create-form').addEventListener('submit', handleCreate);
    else if (p.startsWith('/view/')) loadDetail();
});