let ws = null;
let monitoredHosts = {};

function togglePhase(phaseId) {
  const phase = document.getElementById(phaseId);
  const content = phase.querySelector(".phase-content");
  content.classList.toggle("collapsed");
}

function addLog(containerId, message, className = "") {
  const log = document.getElementById(containerId);
  const line = document.createElement("div");
  line.className = "status-line " + className;
  line.textContent = `[${new Date().toLocaleTimeString()}] ${message}`;
  log.appendChild(line);
  log.scrollTop = log.scrollHeight;
}

function connectWebSocket() {
  const url = document.getElementById("serverUrl").value;

  try {
    ws = new WebSocket(url);

    ws.onopen = () => {
      addLog("connectionLog", "✅ Conectado ao servidor!", "status-connected");
      document.getElementById("connectBtn").disabled = true;
      document.getElementById("firstMessageButton").disabled = false;
      document.getElementById("disconnectBtn").disabled = false;
      document.getElementById("monitorBtn").disabled = false;
    };

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      console.log("Received:", data);
      if (data.host || data.info) {
        addLog(
          "messageLog",
          `📨 Mensagem: ${JSON.stringify(data)}`,
          "status-message"
        );
      } else {
        addLog(
          "firstMessageLog",
          `📨 Mensagem: ${JSON.stringify(data)}`,
          "status-message"
        );
      }

      if (data.host && data.tcp !== undefined) {
        updateHostStatus(data.host, data.tcp);
      }
    };

    ws.onerror = (error) => {
      addLog("connectionLog", "❌ Erro na conexão", "status-error");
    };

    ws.onclose = () => {
      addLog(
        "connectionLog",
        "🔌 Desconectado do servidor",
        "status-disconnected"
      );
      document.getElementById("connectBtn").disabled = false;
      document.getElementById("disconnectBtn").disabled = true;
      document.getElementById("firstMessageButton").disabled = true;
      document.getElementById("monitorBtn").disabled = true;
    };
  } catch (error) {
    addLog("connectionLog", `❌ Erro: ${error.message}`, "status-error");
  }
}

function disconnectWebSocket() {
  if (ws) {
    ws.close();
    ws = null;
    monitoredHosts = {};
    document.getElementById("hostList").innerHTML = "";
  }
}

function sendFirstMessage() {
  const message = document.getElementById("messageInput").value;

  if (!message) {
    alert("Digite um host para monitorar!");
    return;
  }

  if (!ws || ws.readyState !== WebSocket.OPEN) {
    alert("Conecte-se ao servidor primeiro!");
    return;
  }

  const messageToServer = {
    cmd: "repeat",
    message: message,
  };

  ws.send(JSON.stringify(messageToServer));
  addLog(
    "firstMessageLog",
    `📤 Enviado: ${JSON.stringify(messageToServer)}`,
    "status-message"
  );
}

function monitorHost() {
  const host = document.getElementById("hostInput").value;
  const interval = parseInt(document.getElementById("intervalInput").value);

  if (!host) {
    alert("Digite um host para monitorar!");
    return;
  }

  if (!ws || ws.readyState !== WebSocket.OPEN) {
    alert("Conecte-se ao servidor primeiro!");
    return;
  }

  const message = {
    cmd: "monitor",
    host: host,
    interval: interval,
  };

  ws.send(JSON.stringify(message));
  addLog(
    "messageLog",
    `📤 Enviado: ${JSON.stringify(message)}`,
    "status-message"
  );

  if (!monitoredHosts[host]) {
    addHostToList(host);
  }
}

function quickMonitor(host) {
  document.getElementById("hostInput").value = host;
  monitorHost();
}

function addHostToList(host) {
  monitoredHosts[host] = { status: "checking" };

  const hostList = document.getElementById("hostList");
  const hostItem = document.createElement("div");
  hostItem.className = "host-item";
  hostItem.id = `host-${host}`;
  hostItem.innerHTML = `
                <div class="host-name">${host}</div>
                <div class="host-status">
                    <div class="status-indicator"></div>
                    <span>Verificando...</span>
                </div>
            `;
  hostList.appendChild(hostItem);
}

function updateHostStatus(host, isOnline) {
  monitoredHosts[host] = { status: isOnline };

  const hostItem = document.getElementById(`host-${host}`);
  if (hostItem) {
    const statusText = isOnline ? "Online ✅" : "Offline ❌";
    const statusClass = isOnline ? "status-online" : "status-offline";

    hostItem.querySelector(".host-status").innerHTML = `
                    <div class="status-indicator ${statusClass}"></div>
                    <span>${statusText}</span>
                `;
  }
}

function saveReflection(number) {
  const text = document.getElementById(`reflection${number}`).value;
  if (text.trim()) {
    document.getElementById(`feedback${number}`).textContent =
      "✅ Reflexão salva! Continue para a próxima fase.";
  } else {
    document.getElementById(`feedback${number}`).textContent =
      "⚠️ Escreva algo antes de salvar!";
    document.getElementById(`feedback${number}`).style.color = "#ff9800";
  }
}

function completeLesson() {
  const q1 = document.getElementById("question1").value;
  const q2 = document.getElementById("question2").value;
  const q3 = document.getElementById("question3").value;

  if (q1.trim() && q2.trim() && q3.trim()) {
    alert(
      "🎉 Parabéns! Você completou o aprendizado de WebSockets!\n\nVocê aprendeu:\n✅ O que são WebSockets\n✅ Como conectar a um servidor\n✅ Como enviar e receber mensagens\n✅ Monitoramento em tempo real\n✅ Aplicações práticas"
    );
  } else {
    alert("📝 Complete todas as reflexões antes de finalizar!");
  }
}

// Colapsar todas as fases exceto a primeira ao carregar
document.addEventListener("DOMContentLoaded", () => {
  const phases = document.querySelectorAll(".phase");
  phases.forEach((phase, index) => {
    if (index > 0) {
      phase.querySelector(".phase-content").classList.add("collapsed");
    }
  });
});
