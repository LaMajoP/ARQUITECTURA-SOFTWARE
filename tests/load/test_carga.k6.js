import http from "k6/http";
import { check, sleep } from "k6";

// ─────────────────────────────────────────────
// Configuracion de la prueba
// ─────────────────────────────────────────────

export const options = {
  stages: [
    { duration: "15s", target: 10 },  
    { duration: "30s", target: 50 },  
    { duration: "15s", target: 50 },
    { duration: "30s", target: 0 },
  ],
  thresholds: {
    http_req_duration: ["p(95)<10000"],  
    http_req_failed:   ["rate<0.10"],   
  },
};

const BASE_URL = "http://localhost:8000";

// ─────────────────────────────────────────────
// Funcion auxiliar: hace login y retorna el token
// ─────────────────────────────────────────────

function obtener_token() {
  const response = http.post(
    `${BASE_URL}/login`,
    JSON.stringify({ username: "admin", password: "admin123" }),
    { headers: { "Content-Type": "application/json" } }
  );

  check(response, {
    "login exitoso": (r) => r.status === 200,
    "token recibido": (r) => JSON.parse(r.body).access_token !== undefined,
  });

  return JSON.parse(response.body).access_token;
}

// ─────────────────────────────────────────────
// Escenario principal - se ejecuta por cada usuario virtual
// ─────────────────────────────────────────────

export default function () {

  // 1. login
  const token = obtener_token();
  const headers = {
    "Content-Type": "application/json",
    "Authorization": `Bearer ${token}`,
  };

  sleep(0.5); // pausa entre requests para simular comportamiento real

  // 2. calcular promedio
  const payload_promedio = JSON.stringify({
    materias: [
      { id: 101, nombre: "Cálculo Univariado",                        creditos: 4, semestre: 1, nota: 3.5, es_oficial: true },
      { id: 102, nombre: "Algoritmos y Fundamentos de Programación",  creditos: 4, semestre: 1, nota: 4.0, es_oficial: true },
      { id: 103, nombre: "Matemáticas Discretas",                     creditos: 3, semestre: 1, nota: 3.8, es_oficial: true },
    ],
  });

  const response_promedio = http.post(
    `${BASE_URL}/promedio`,
    payload_promedio,
    { headers }
  );

  check(response_promedio, {
    "promedio status 200":          (r) => r.status === 200,
    "promedio_calculado en respuesta": (r) => JSON.parse(r.body).promedio_calculado !== undefined,
  });

  sleep(0.5);

  // 3. calcular promedio objetivo (solo admin)
  const payload_objetivo = JSON.stringify({
    materias_cursadas: [
      { id: 101, nombre: "Cálculo Univariado", creditos: 4, semestre: 1, nota: 3.5, es_oficial: true },
    ],
    materias_pendientes: [
      { id: 102, nombre: "Física", creditos: 4, semestre: 2, nota: 0.0, es_oficial: true },
    ],
    promedio_objetivo: 4.0,
  });

  const response_objetivo = http.post(
    `${BASE_URL}/promedio-objetivo`,
    payload_objetivo,
    { headers }
  );

  check(response_objetivo, {
    "objetivo status 200": (r) => r.status === 200,
    "nota_requerida en respuesta": (r) => JSON.parse(r.body).nota_requerida_en_pendientes !== undefined,
  });

  sleep(1); // pausa al final de cada iteracion
}