
function mask(o, f) {
    setTimeout(function () {
        var v = mphone(o.value);
        if (v != o.value) {
            o.value = v;
        }
    }, 1);
}
function mphone(v) {
    var r = v.replace(/\D/g, "");
    r = r.replace(/^0/, "");
    if (r.length > 10) {
        r = r.replace(/^(\d\d)(\d{5})(\d{4}).*/, "($1) $2-$3");
    } else if (r.length > 5) {
        r = r.replace(/^(\d\d)(\d{4})(\d{0,4}).*/, "($1) $2-$3");
    } else if (r.length > 2) {
        r = r.replace(/^(\d\d)(\d{0,5})/, "($1) $2");
    } else {
        r = r.replace(/^(\d*)/, "($1");
    }
    return r;
}


function enviar() {
    nome = document.getElementById("id").value;

    var url_atual = window.location.href;

    if (url_atual == "/usuarios/" + nome + "") {
        window.location.href = "/usuarios";
    } else {
        window.location.href = "/usuarios/editar/" + nome + "";
    }
}

function deletar() {
    id = document.getElementById("id").value;
    window.location.href = "/usuarios/deletar/confirm/" + id + "";
}
function renovar() {
    id = document.getElementById("id").value;
    mes = document.getElementById("mes").value;
    window.location.href = "/renovar/" + id + "/"+ mes + "";
}


function pesquisar(){
    var categoria = document.getElementById("select_pesquisa").value
    var pesquisa = document.getElementById("pesquisa").value

    if(pesquisa.length > 0){
        window.location.href = "/usuarios/" + categoria + "/" +pesquisa+ "";
    } else {
        alert("Digite a palavra chave para pesquisa")
    }
}


function ordenar_vencimento(){
    window.location.href = "/usuarios/ordenar/vencimento";
}
function ordenar_adicionado(){
    window.location.href = "/usuarios/ordenar/adicionado";
}
function ordenar_id(){
    window.location.href = "/usuarios/ordenar/id";
}
function ordenar_nome(){
    window.location.href = "/usuarios/ordenar/nome";
}
function ordenar_numero(){
    window.location.href = "/usuarios/ordenar/numero";
}
function ordenar_valor(){
    window.location.href = "/usuarios/ordenar/valor";
}
function ordenar_plano(){
    window.location.href = "/usuarios/ordenar/plano";
}

function view_opcao(){
    document.getElementById("opcoes").style.display = "block"
}

function view_account(){
    var atual = document.getElementById("account").style.display
    
    if(atual=="block"){
        document.getElementById("account").style.display = "none"
    } else {
        var atual = document.getElementById("account").style.display = "block"
    }
}