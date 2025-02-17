window.addEventListener('load', () => {
    carregarCidades();
    initializeEventListeners();
});

function getSensationClass(sensacao_termica) {
    if (sensacao_termica >= 30) return 'hot';
    if (sensacao_termica >= 25) return 'warm';
    if (sensacao_termica>= 15) return 'comfortable';
    return 'cold'; 
}

function getSensationMessage(sensacao_termica) {
    if (sensacao_termica >= 30) return 'Sensação de muito calor. Mantenha-se hidratado!';
    if (sensacao_termica >= 25) return 'Sensação de calor moderado.';
    if (sensacao_termica >= 15) return 'Clima confortável.';
    return 'Sensação de frio. Prepare-se para o inverno!'; 
}

function carregarCidades() {
    fetch('/cidades')
        .then(response => response.json())
        .then(cidades => {
            const select = document.getElementById('cidade');
            cidades.forEach(cidade => {
                const option = document.createElement('option');
                option.value = cidade;
                option.textContent = cidade;
                select.appendChild(option);
            });
        })
        .catch(error => {
            console.error('Error loading cities:', error);
            document.getElementById('error').textContent = 'Erro ao carregar cidades';
            document.getElementById('error').style.display = 'block';
        });
}

function initializeEventListeners() {
    const citySelect = document.getElementById('cidade');
    citySelect.addEventListener('change', buscarClima);
}

function buscarClima() {
    const cidade = document.getElementById('cidade').value;
    const resultadoDiv = document.getElementById('resultado');
    const errorDiv = document.getElementById('error');
    
    if (!cidade) {
        errorDiv.textContent = 'Por favor, selecione uma cidade';
        errorDiv.style.display = 'block';
        resultadoDiv.style.display = 'none';
        return;
    }

    fetch(`/buscar?cidade=${encodeURIComponent(cidade)}`)
        .then(response => response.json())
        .then(data => {
            console.log("Received data:", data); 
            console.log('Received data:', JSON.stringify(data, null, 2));
            
            if (data.error) {
                errorDiv.textContent = data.error;
                errorDiv.style.display = 'block';
                resultadoDiv.style.display = 'none';
                return;
            }

            document.getElementById('cidade-nome').textContent = data.cidade;
            document.getElementById('temperatura').textContent = data.temperatura.toFixed(1);
            document.getElementById('sensacao-termica').textContent = data.sensacao_termica.toFixed(1);
            document.getElementById('umidade').textContent = data.umidade;
            document.getElementById('precipitacao').textContent = data.precipitacao.toFixed(1);
            document.getElementById('data').textContent = new Date(data.data).toLocaleString();
            
            const sensationInfo = document.getElementById('sensation-info');
            sensationInfo.className = 'sensation-info ' + getSensationClass(data.sensacao_termica);
            sensationInfo.textContent = getSensationMessage(data.sensacao_termica);
            
            errorDiv.style.display = 'none';
            resultadoDiv.style.display = 'block';

            updateBackground(data.sensacao_termica);  
        })
        .catch(error => {
            errorDiv.textContent = 'Erro ao buscar dados do clima';
            errorDiv.style.display = 'block';
            resultadoDiv.style.display = 'none';
            console.error('Error:', error);
        });
}

function updateBackground(sensacao_termica) {
    let body = document.body;
    
    console.log("Updating background based on sensacao_termica:", sensacao_termica);
    
    sensacao_termica = Number(sensacao_termica);

    console.log("Before update:", body.classList.toString());

    body.classList.remove("bg-cold", "bg-warm", "bg-hot", "bg-comfortable");

    void body.offsetWidth;

    setTimeout(() => {
        if (sensacao_termica < 15) {
            body.classList.add("bg-cold");
        } else if (sensacao_termica > 30) {
            body.classList.add("bg-hot");
        } else if (sensacao_termica >= 15 && sensacao_termica < 25) {
            body.classList.add("bg-comfortable"); 
        } else {
            body.classList.add("bg-warm");
        }

        console.log("After update:", body.classList.toString());

        void body.offsetWidth;
    }, 10);
}