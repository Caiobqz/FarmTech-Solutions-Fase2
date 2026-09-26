#include <DHTesp.h>

// =========================
// FarmTech Solutions - Fase 2
// ESP32 + Wokwi
// Cultura: Cafe arabica
// =========================

#define PIN_N 18
#define PIN_P 19
#define PIN_K 21
#define PIN_LDR 34
#define PIN_DHT 15
#define PIN_RELE 23

const float PH_MIN = 5.5;
const float PH_MAX = 6.0;
const float UMIDADE_LIMITE = 50.0;

DHTesp dht;

// Resultado do programa Python/API.
// false = sem chuva prevista; true = chuva prevista.
bool chuvaPrevista = false;

unsigned long ultimaLeitura = 0;
const unsigned long INTERVALO_LEITURA = 2500;

float converterLdrParaPh(int valorAnalogico) {
  // Conversao DIDATICA solicitada pela atividade.
  // O LDR mede luz, nao pH.
  return (valorAnalogico / 4095.0) * 14.0;
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
  } else if (comando == "CHUVA=NAO" || comando == "CHUVA=0" || comando == "CHUVA=FALSE") {
    chuvaPrevista = false;
    Serial.println("[API] Chuva prevista: NAO");
  } else if (comando == "STATUS") {
    Serial.print("[STATUS] Chuva prevista = ");
    Serial.println(chuvaPrevista ? "SIM" : "NAO");
  } else {
    Serial.println("[COMANDO] Use CHUVA=SIM, CHUVA=NAO ou STATUS.");
  }
}

void imprimirSeparador() {
  Serial.println("----------------------------------------");
}

void setup() {
  Serial.begin(115200);

  pinMode(PIN_N, INPUT_PULLUP);
  pinMode(PIN_P, INPUT_PULLUP);
  pinMode(PIN_K, INPUT_PULLUP);
  pinMode(PIN_LDR, INPUT);
  pinMode(PIN_RELE, OUTPUT);

  digitalWrite(PIN_RELE, LOW);

  // Biblioteca recomendada pelo Wokwi para DHT22 + ESP32.
  dht.setup(PIN_DHT, DHTesp::DHT22);

  Serial.println();
  Serial.println("========================================");
  Serial.println(" FARMTECH SOLUTIONS - FASE 2");
  Serial.println(" Sistema de irrigacao inteligente");
  Serial.println(" Cultura: Cafe arabica");
  Serial.println("========================================");
  Serial.println("Comandos: CHUVA=SIM | CHUVA=NAO | STATUS");
  Serial.println();
}

void loop() {
  processarComandoSerial();

  if (millis() - ultimaLeitura < INTERVALO_LEITURA) {
    delay(20);
    return;
  }
  ultimaLeitura = millis();

  // INPUT_PULLUP: pressionado = LOW.
  bool nitrogenioAdequado = digitalRead(PIN_N) == LOW;
  bool fosforoAdequado = digitalRead(PIN_P) == LOW;
  bool potassioAdequado = digitalRead(PIN_K) == LOW;

  int valorLdr = analogRead(PIN_LDR);
  float phSimulado = converterLdrParaPh(valorLdr);

  TempAndHumidity dadosDht = dht.getTempAndHumidity();
  float umidade = dadosDht.humidity;
  float temperatura = dadosDht.temperature;

  // Em caso de falha do sensor, a bomba e mantida desligada por seguranca.
  if (isnan(umidade) || isnan(temperatura)) {
    Serial.println("ERRO: nao foi possivel ler o DHT22.");
    digitalWrite(PIN_RELE, LOW);
    return;
  }

  bool phAdequado = phSimulado >= PH_MIN && phSimulado <= PH_MAX;
  bool soloSeco = umidade < UMIDADE_LIMITE;

  // Regra principal:
  // irrigar quando a umidade estiver baixa e nao houver chuva prevista.
  bool irrigar = soloSeco && !chuvaPrevista;

  digitalWrite(PIN_RELE, irrigar ? HIGH : LOW);

  imprimirSeparador();
  Serial.println("LEITURA DOS SENSORES");
  Serial.print("N: ");
  Serial.println(nitrogenioAdequado ? "ADEQUADO" : "INADEQUADO");
  Serial.print("P: ");
  Serial.println(fosforoAdequado ? "ADEQUADO" : "INADEQUADO");
  Serial.print("K: ");
  Serial.println(potassioAdequado ? "ADEQUADO" : "INADEQUADO");
  Serial.print("LDR: ");
  Serial.println(valorLdr);
  Serial.print("pH simulado: ");
  Serial.println(phSimulado, 2);
  Serial.print("Temperatura DHT22: ");
  Serial.print(temperatura, 1);
  Serial.println(" C");
  Serial.print("Umidade simulada: ");
  Serial.print(umidade, 1);
  Serial.println(" %");
  Serial.print("Chuva prevista: ");
  Serial.println(chuvaPrevista ? "SIM" : "NAO");

  Serial.println();
  Serial.println("ALERTAS AGRONOMICOS");
  if (!nitrogenioAdequado) Serial.println("- Nitrogenio inadequado.");
  if (!fosforoAdequado) Serial.println("- Fosforo inadequado.");
  if (!potassioAdequado) Serial.println("- Potassio inadequado.");
  if (!phAdequado) Serial.println("- pH fora da faixa simulada de 5,5 a 6,0.");
  if (nitrogenioAdequado && fosforoAdequado && potassioAdequado && phAdequado) {
    Serial.println("- Nenhum alerta de NPK/pH.");
  }

  Serial.println();
  Serial.println("DECISAO DE IRRIGACAO");
  if (irrigar) {
    Serial.println("RELE: ON -> BOMBA LIGADA");
    Serial.println("Motivo: umidade abaixo de 50% e sem chuva prevista.");
  } else if (chuvaPrevista && soloSeco) {
    Serial.println("RELE: OFF -> BOMBA DESLIGADA");
    Serial.println("Motivo: umidade baixa, mas existe chuva prevista.");
  } else {
    Serial.println("RELE: OFF -> BOMBA DESLIGADA");
    Serial.println("Motivo: umidade igual ou superior a 50%.");
  }
}
