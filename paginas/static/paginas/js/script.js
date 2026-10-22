/**
 * JavaScript do formulário de Contato / Ouvidoria (mantido da ATV07).
 * A navegação entre páginas NÃO usa JavaScript: ela é feita pelas URLs do Django.
 * Este script só age quando a página atual possui o formulário #formContato.
 */
document.addEventListener('DOMContentLoaded', function () {
    var form = document.getElementById('formContato');
    if (!form) {
        return; // outras páginas não têm formulário
    }

    form.addEventListener('submit', interceptarEnvio);

    var btnVoltar = document.getElementById('btnVoltar');
    if (btnVoltar) {
        btnVoltar.addEventListener('click', voltarParaFormulario);
    }

    processarDadosURL();
});

/** Valida, mostra o resumo em confirm() e só envia (GET) se o usuário confirmar. */
function interceptarEnvio(event) {
    event.preventDefault();

    var form = document.getElementById('formContato');

    if (!form.checkValidity()) {
        form.reportValidity();
        return false;
    }

    var nome = document.getElementById('nome').value.trim();
    var email = document.getElementById('email').value.trim();
    var telefone = document.getElementById('telefone').value.trim();
    var selectAssunto = document.getElementById('assunto');
    var assuntoSelecionado = selectAssunto.options[selectAssunto.selectedIndex].text;
    var perfil = document.querySelector('input[name="perfil"]:checked');
    var perfilSelecionado = perfil ? perfil.value : 'Não informado';
    var mensagem = document.getElementById('mensagem').value.trim();

    var resumo = 'RESUMO DA MENSAGEM\n\n' +
        'Nome: ' + nome + '\n' +
        'E-mail: ' + email + '\n' +
        'Telefone: ' + telefone + '\n' +
        'Assunto: ' + assuntoSelecionado + '\n' +
        'Perfil: ' + perfilSelecionado + '\n' +
        'Mensagem: ' + mensagem.substring(0, 50) + (mensagem.length > 50 ? '...' : '') + '\n\n' +
        'Deseja confirmar o envio?';

    if (confirm(resumo)) {
        form.submit(); // envia via GET para a mesma página
        return true;
    }

    alert('Envio cancelado. Você pode editar suas informações.');
    return false;
}

/** Se a URL tem ?nome=...&email=..., mostra a mensagem de sucesso no lugar do formulário. */
function processarDadosURL() {
    var params = new URLSearchParams(window.location.search);
    var nome = params.get('nome');
    var email = params.get('email');

    if (!(nome && email)) {
        return;
    }

    document.querySelector('.formulario-container').style.display = 'none';
    document.getElementById('pagina-sucesso').classList.add('ativa');

    // textContent (e não innerHTML) evita que o usuário injete HTML na página
    var dados = document.getElementById('dadosSucesso');
    dados.textContent = '';

    var p1 = document.createElement('p');
    p1.style.fontSize = '20px';
    p1.style.marginBottom = '15px';
    p1.textContent = '🎉 Olá, ' + nome + '! 🎉';

    var p2 = document.createElement('p');
    p2.textContent = 'Recebemos sua mensagem com sucesso!';

    var p3 = document.createElement('p');
    p3.textContent = '📧 E-mail: ' + email;

    var p4 = document.createElement('p');
    p4.style.marginTop = '15px';
    p4.textContent = 'Agradecemos pelo seu contato. Em breve retornaremos.';

    dados.append(p1, p2, p3, p4);

    // Limpa a URL para que, ao recarregar, o formulário volte
    if (window.history && window.history.replaceState) {
        window.history.replaceState({}, document.title, window.location.pathname);
    }
}

/** Botão "Voltar para o Formulário". */
function voltarParaFormulario() {
    document.getElementById('pagina-sucesso').classList.remove('ativa');
    document.querySelector('.formulario-container').style.display = '';
    document.getElementById('formContato').reset();
}
