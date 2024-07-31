document.addEventListener('DOMContentLoaded', function() {
    function loadOrders() {
        fetch('/listarTodosPedidos')
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    document.getElementById('ordersContainer').innerHTML = `<p style="color:red;">Erro: ${data.error}</p>`;
                } else {
                    const ordersTableBody = document.getElementById('ordersTableBody');
                    ordersTableBody.innerHTML = '';
                    data.forEach(order => {
                        const row = document.createElement('tr');
                        row.innerHTML = `
                            <td>${order._id}</td>
                            <td>${order.cpf}</td>
                            <td>${order.itens.map(item => `${item.nome} (R$ ${item.price})`).join(', ')}</td>
                            <td>R$ ${order.total_price.toFixed(2)}</td>
                            <td>${order.status}</td>
                            <td>${new Date(order.created_at).toLocaleString('pt-BR')}</td>
                            <td>${order.paid_at ? new Date(order.paid_at).toLocaleString('pt-BR') : 'N/A'}</td>
                        `;
                        ordersTableBody.appendChild(row);
                    });
                }
            })
            .catch(error => {
                console.error('Erro ao carregar os pedidos:', error);
                document.getElementById('ordersContainer').innerHTML = `<p style="color:red;">Erro ao carregar pedidos.</p>`;
            });
    }

    function processSalesAnalysis(event) {
        event.preventDefault();
        const dataInicio = document.getElementById('data_inicio').value;
        const dataFim = document.getElementById('data_fim').value;

        fetch(`/salesAnalysis?data_inicio=${dataInicio}&data_fim=${dataFim}`)
            .then(response => response.json())
            .then(data => {
                console.log('Dados recebidos:', data);

                if (data.error) {
                    document.getElementById('resultado-analise').innerHTML = `<p style="color:red;">Erro: ${data.error}</p>`;
                } else {
                    const ctx = document.getElementById('salesChart').getContext('2d');
                    const salesChart = new Chart(ctx, {
                        type: 'line',
                        data: {
                            labels: data.sales.map(sale => sale.date),
                            datasets: [{
                                label: 'Vendas',
                                data: data.sales.map(sale => sale.amount),
                                borderColor: 'rgba(75, 192, 192, 1)',
                                borderWidth: 1,
                                fill: false
                            }]
                        },
                        options: {
                            scales: {
                                x: {
                                    beginAtZero: true
                                },
                                y: {
                                    beginAtZero: true
                                }
                            }
                        }
                    });

                    document.getElementById('totalSales').innerText = `R$ ${data.totalSales.toFixed(2)}`;
                    document.getElementById('averageSales').innerText = `R$ ${data.averageSales.toFixed(2)}`;
                    document.getElementById('salesCount').innerText = data.salesCount;
                }
            })
            .catch(error => {
                console.error('Erro ao carregar a análise de vendas:', error);
                document.getElementById('resultado-analise').innerHTML = `<p style="color:red;">Erro ao carregar a análise de vendas.</p>`;
            });
    }

    document.getElementById('pedidos-tab').addEventListener('click', loadOrders);
    document.getElementById('salesAnalysisForm').addEventListener('submit', processSalesAnalysis);
});
