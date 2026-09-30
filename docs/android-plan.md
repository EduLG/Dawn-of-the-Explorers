# Plan de la app Android

Contexto compartido entre Edu y el agente para llevar Dawn of the Explorers a Android. El detalle de cada tarea vive en Jira, proyecto `DOTE` (https://eduladron.atlassian.net/browse/DOTE).

## Decisiones

- **Capacitor, no reescritura.** La app Android empaqueta el frontend React actual dentro de un WebView. El código del juego es el mismo que el de la web.
- **Un repo, dos salidas.** La web sigue desplegándose en Vercel como hasta ahora. La APK es un segundo build del mismo `frontend-react/`.
- **Siempre online.** La app se conecta por HTTPS al mismo backend que la web (Railway), con las mismas cuentas y datos. No hay modo offline.
- **Backend casi intacto.** El único cambio necesario es que el CORS acepte también el origen de la app, `https://localhost`.

## Fases

| Fase | Épica | Resultado |
| --- | --- | --- |
| 1. Preparar el repositorio | DOTE-1 | Repo limpio (`venv/` y `.env` fuera de git) y documentación al día |
| 2. Frontend usable en móvil | DOTE-2 | Todas las pantallas funcionan a 360 px de ancho, sin cambiar el escritorio |
| 3. Empaquetar con Capacitor y conectar al servidor | DOTE-3 | APK debug que hace login, equipa y explora contra producción |
| 4. Ajustes nativos de Android | DOTE-4 | Botón atrás, icono, splash, sesión persistente, notificaciones de exploración |
| 5. Build firmado y distribución | DOTE-5 | APK de release firmada, probada en un dispositivo real y publicada |

## Datos de producción

- Web: https://dawn-of-the-explorers.vercel.app
- Backend: https://valiant-communication-production-1dc5.up.railway.app
- Origen desde el que la app Android hace las peticiones: `https://localhost`

## Forma de trabajo

- El agente explica cada paso antes de hacerlo y espera confirmación.
- **Las operaciones de git las hace solo Edu:** crear ramas, commits, merges, push, pull requests y tags. El agente no ejecuta ninguna de ellas; deja los cambios sin confirmar en el directorio de trabajo, explica qué ha tocado y sugiere cuándo toca cada operación (por ejemplo: "este es buen momento para un commit" o "esta tarea conviene hacerla en una rama nueva desde `develop`").
- Como referencia para esas sugerencias: una rama por tarea o grupo pequeño de tareas, creada desde `develop` y fusionada de vuelta en `develop`. La decisión final es de Edu.
- Los despliegues y los cambios de variables en producción (Railway, Vercel) también los hace solo Edu; el agente indica cuándo hacen falta y qué hay que cambiar.
- Cada tarea de Jira tiene un criterio "Hecho cuando" que se comprueba antes de cerrarla.
- Los cambios de la fase 2 se comprueban siempre en ancho móvil y en escritorio, porque el código es compartido con la web.
- Tareas manuales de Edu: instalar Android Studio (DOTE-22), desplegar y configurar variables en Railway (DOTE-26), generar y custodiar la keystore (DOTE-42), probar en el teléfono (DOTE-44) y elegir el canal de distribución (DOTE-47).

## Riesgos a vigilar

- Las tareas que tocan código compartido con la web son la navegación principal (DOTE-14), el almacenamiento de tokens (DOTE-35, DOTE-36) y el CORS (DOTE-25).
- Un cambio incompatible en la API puede romper las APK ya instaladas, que no se actualizan solas.
- La keystore de firma no debe entrar nunca en git ni perderse.
