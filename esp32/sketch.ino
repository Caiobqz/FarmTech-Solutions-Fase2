#include <DHTesp.h>

// FarmTech Solutions - Fase 2
// ESP32 + Wokwi | Cultura: cafe arabica

// -------------------------
// Pinos
// -------------------------
constexpr uint8_t PIN_N = 18;
constexpr uint8_t PIN_P = 19;
constexpr uint8_t PIN_K = 21;
constexpr uint8_t PIN_LDR = 34;
constexpr uint8_t PIN_DHT = 15;
constexpr uint8_t PIN_RELE = 23;

// -------------------------
// Regras da simulacao
// -------------------------
constexpr float PH_MIN = 5.5;
constexpr float PH_MAX = 6.0;
constexpr float UMIDADE_LIMITE = 50.0;
constexpr unsigned long INTERVALO_LEITURA_MS = 2500;

// O circuito atual assume rele ativo em HIGH.
// Confirmar esse comportamento durante a validacao no Wokwi.
constexpr uint8_t RELE_LIGADO = HIGH;
constexpr uint8_t RELE_DESLIGADO = LOW;

DHTesp dht;

bool chuvaPrevista = false;
unsigned long ultimaLeitura = 0;

// Agrupa as leituras para manter o loop principal simples.
struct LeiturasSensores {
  bool nitrogenioAdequado;
  bool fosforoAdequado;
  bool potassioAdequado;
  int valorLdr;
  float phSimulado;
  float umidade;
  float temperatura;
};

bool nutrienteAdequado(uint8_t pino) {
  // INPUT_PULLUP: pressionado = LOW.
  return digitalRead(pino) == LOW;
}

float converterLdrParaPh(int valorAnalogico) {
  // Conversao didatica: o LDR mede luz, nao pH.
  return (valorAnalogico / 4095.0) * 14.0;
}

bool phEstaAdequado(float ph) {
  return ph >= PH_MIN && ph <= PH_MAX;
}

bool leituraDhtValida(const LeiturasSensores& leituras) {
  return !isnan(leituras.umidade) && !isnan(leituras.temperatura);
}

bool soloEstaSeco(float umidade) {
  return umidade < UMIDADE_LIMITE;
}

bool deveIrrigar(float umidade) {
  return soloEstaSeco(umidade) && !chuvaPrevista;
}

void atualizarRele(bool ligar) {
  digitalWrite(PIN_RELE, ligar ? RELE_LIGADO : RELE_DESLIGADO);
}

LeiturasSensores lerSensores() {
  LeiturasSensores leituras;

  leituras.nitrogenioAdequado = nutrienteAdequado(PIN_N);
  leituras.fosforoAdequado = nutrienteAdequado(PIN_P);
  leituras.potassioAdequado = nutrienteAdequado(PIN_K);

  leituras.valorLdr = analogRead(PIN_LDR);
  leituras.phSimulado = converterLdrParaPh(leituras.valorLdr);

  const TempAndHumidity dadosDht = dht.getTempAndHumidity();
  leituras.umidade = dadosDht.humidity;
  leituras.temperatura = dadosDht.temperature;

  return leituras;
}

void processarComandoSerial() {
  if (!Serial.available()) {
    return;
  }

  String comando = Serial.readStringUntil('\n');
  comando.trim();
  comando.toUpperCase();

  if (comando == "CHUVA=SIM" || comando == "CHUVA=1" || comando == "CHUVA=TRUE") {
    chuvaPrevista = true;
    Serial.println("[API] Chuva prevista: SIM");
    return;
  }

  if (comando == "CHUVA=NAO" || comando == "CHUVA=0" || comando == "CHUVA=FALSE") {
    chuvaPrevista = false;
    Serial.println("[API] Chuva prevista: NAO");
    return;
  }

  if (comando == "STATUS") {
    Serial.print("[STATUS] Chuva prevista = ");
    Serial.println(chuvaPrevista ? "SIM" : "NAO");
    return;
  }

  Serial.println("[COMANDO] Use CHUVA=SIM, CHUVA=NAO ou STATUS.");
}

void imprimirLeituras(const LeiturasSensores& leituras) {
  Serial.println("----------------------------------------");
  Serial.println("LEITURA DOS SENSORES");

  Serial.print("N: ");
  Serial.println(leituras.nitrogenioAdequado ? "ADEQUADO" : "INADEQUADO");

  Serial.print("P: ");
  Serial.println(leituras.fosforoAdequado ? "ADEQUADO" : "INADEQUADO");

  Serial.print("K: ");
  Serial.println(leituras.potassioAdequado ? "ADEQUADO" : "INADEQUADO");

  Serial.print("LDR: ");
  Serial.println(leituras.valorLdr);

  Serial.print("pH simulado: ");
  Serial.println(leituras.phSimulado, 2);

  Serial.print("Temperatura DHT22: ");
  Serial.print(leituras.temperatura, 1);
  Serial.println(" C");

  Serial.print("Umidade simulada: ");
  Serial.print(leituras.umidade, 1);
  Serial.println(" %");

  Serial.print("Chuva prevista: ");
  Serial.println(chuvaPrevista ? "SIM" : "NAO");
}

void imprimirAlertas(const LeiturasSensores& leituras) {
  const bool phAdequado = phEstaAdequado(leituras.phSimulado);
  const bool semAlertas =
      leituras.nitrogenioAdequado &&
      leituras.fosforoAdequado &&
      leituras.potassioAdequado &&
      phAdequado;

  Serial.println();
  Serial.println("ALERTAS AGRONOMICOS");

  if (!leituras.nitrogenioAdequado) {
    Serial.println("- Nitrogenio inadequado.");
  }

  if (!leituras.fosforoAdequado) {
    Serial.println("- Fosforo inadequado.");
  }

  if (!leituras.potassioAdequado) {
    Serial.println("- Potassio inadequado.");
  }

  if (!phAdequado) {
    Serial.println("- pH fora da faixa simulada de 5,5 a 6,0.");
  }

  if (semAlertas) {
    Serial.println("- Nenhum alerta de NPK/pH.");
  }
}

void imprimirDecisao(float umidade, bool irrigar) {
  Serial.println();
  Serial.println("DECISAO DE IRRIGACAO");

  if (irrigar) {
    Serial.println("RELE: ON -> BOMBA LIGADA");
    Serial.println("Motivo: umidade abaixo de 50% e sem chuva prevista.");
    return;
  }

  Serial.println("RELE: OFF -> BOMBA DESLIGADA");

  if (soloEstaSeco(umidade) && chuvaPrevista) {
    Serial.println("Motivo: umidade baixa, mas existe chuva prevista.");
  } else {
    Serial.println("Motivo: umidade igual ou superior a 50%.");
  }
}

void imprimirCabecalho() {
  Serial.println();
  Serial.println("========================================");
  Serial.println(" FARMTECH SOLUTIONS - FASE 2");
  Serial.println(" Sistema de irrigacao inteligente");
  Serial.println(" Cultura: cafe arabica");
  Serial.println("========================================");
  Serial.println("Comandos: CHUVA=SIM | CHUVA=NAO | STATUS");
  Serial.println();
}

void setup() {
  Serial.begin(115200);

  pinMode(PIN_N, INPUT_PULLUP);
  pinMode(PIN_P, INPUT_PULLUP);
  pinMode(PIN_K, INPUT_PULLUP);
  pinMode(PIN_LDR, INPUT);
  pinMode(PIN_RELE, OUTPUT);

  atualizarRele(false);
  dht.setup(PIN_DHT, DHTesp::DHT22);

  imprimirCabecalho();
}

void loop() {
  processarComandoSerial();

  if (millis() - ultimaLeitura < INTERVALO_LEITURA_MS) {
    delay(20);
    return;
  }

  ultimaLeitura = millis();

  const LeiturasSensores leituras = lerSensores();

  if (!leituraDhtValida(leituras)) {
    atualizarRele(false);
    Serial.println("ERRO: nao foi possivel ler o DHT22.");
    return;
  }

  const bool irrigar = deveIrrigar(leituras.umidade);

  atualizarRele(irrigar);
  imprimirLeituras(leituras);
  imprimirAlertas(leituras);
  imprimirDecisao(leituras.umidade, irrigar);
}
