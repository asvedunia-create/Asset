async function fetchAssets() {
  const res = await fetch('/api/assets');
  const data = await res.json();
  renderRows(data);
}

function renderRows(items) {
  const tbody = document.getElementById('assetRows');
  tbody.innerHTML = '';

  for (const asset of items) {
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td>${asset.hostname}</td>
      <td>${asset.address}</td>
      <td>${asset.protocol}</td>
      <td>${asset.os_name}</td>
      <td>${asset.owner}</td>
      <td>${asset.services.map(s => `${s.name} ${s.version}`).join('<br/>')}</td>
    `;
    tbody.appendChild(tr);
  }
}

async function refreshAssets() {
  const payloadText = document.getElementById('payload').value;
  let payload;

  try {
    payload = JSON.parse(payloadText);
  } catch (_err) {
    alert('Некоректний JSON payload');
    return;
  }

  const res = await fetch('/api/assets/refresh', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });

  if (!res.ok) {
    const text = await res.text();
    alert(`Помилка refresh: ${text}`);
    return;
  }

  await fetchAssets();
}

document.getElementById('refreshBtn').addEventListener('click', refreshAssets);
fetchAssets();
