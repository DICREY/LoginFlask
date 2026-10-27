"""
Base de conocimiento interna sobre desarrollo de aplicaciones móviles.

Se carga en SQLite al arrancar (ver mobile.seed_mobile_data). Para añadir o
corregir contenido basta con editar estas listas y reiniciar el servidor:
los registros se actualizan por `slug`.
"""

PLATFORMS = [
    {
        "slug": "android",
        "name": "Android",
        "vendor": "Google",
        "languages": ["Kotlin", "Java", "C/C++ (NDK)"],
        "ide": "Android Studio",
        "store": "Google Play",
        "package_formats": ["AAB (publicación en Google Play)", "APK (instalación directa)"],
        "developer_fee": "Pago único de 25 USD para la cuenta de Google Play Console",
        "market_share": "≈70–73 % de los dispositivos móviles a nivel mundial (StatCounter, aprox.)",
        "summary": (
            "Sistema operativo móvil basado en Linux y de código abierto (AOSP). "
            "Lo usan muchos fabricantes (Samsung, Xiaomi, Motorola, Google Pixel...), "
            "por lo que hay mucha variedad de pantallas, versiones y capacidades de hardware."
        ),
        "key_points": [
            "Se desarrolla con Kotlin y Jetpack Compose para la interfaz.",
            "La compatibilidad se controla con minSdk / targetSdk (niveles de API).",
            "Google Play exige subir apps nuevas en formato AAB y apuntar a un targetSdk reciente.",
            "La fragmentación obliga a probar en varios tamaños de pantalla y versiones del sistema.",
        ],
    },
    {
        "slug": "ios",
        "name": "iOS / iPadOS",
        "vendor": "Apple",
        "languages": ["Swift", "Objective-C"],
        "ide": "Xcode (solo en macOS)",
        "store": "App Store",
        "package_formats": ["IPA"],
        "developer_fee": "Apple Developer Program: 99 USD al año",
        "market_share": "≈27–30 % a nivel mundial; mayoritario en EE. UU., Japón y otros mercados (aprox.)",
        "summary": (
            "Sistema operativo cerrado de Apple para iPhone y iPad. Pocos modelos de "
            "dispositivo y una adopción rápida de nuevas versiones simplifican las pruebas, "
            "pero publicar requiere una Mac, una cuenta de desarrollador y pasar la revisión de Apple."
        ),
        "key_points": [
            "Se desarrolla con Swift y SwiftUI (o UIKit en proyectos más antiguos).",
            "Toda app debe firmarse con certificados y perfiles de aprovisionamiento.",
            "TestFlight permite distribuir versiones beta a testers antes de publicar.",
            "La revisión de App Store aplica las App Review Guidelines (privacidad, pagos, contenido).",
        ],
    },
]

FRAMEWORKS = [
    {
        "slug": "jetpack-compose",
        "name": "Jetpack Compose",
        "type": "nativo",
        "company": "Google",
        "language": "Kotlin",
        "platforms": ["Android"],
        "first_release": "2021 (versión estable)",
        "summary": "Toolkit declarativo moderno para construir interfaces nativas en Android.",
        "pros": [
            "Recomendado oficialmente por Google para nuevas apps Android",
            "Menos código que el sistema de vistas XML",
            "Vista previa en Android Studio e interoperabilidad con vistas clásicas",
        ],
        "cons": ["Solo Android (para iOS ver Compose Multiplatform)", "Curva de aprendizaje del modelo de recomposición"],
        "use_when": "La app es solo para Android o se busca la mejor integración con el sistema.",
    },
    {
        "slug": "swiftui",
        "name": "SwiftUI",
        "type": "nativo",
        "company": "Apple",
        "language": "Swift",
        "platforms": ["iOS", "iPadOS", "macOS", "watchOS", "tvOS", "visionOS"],
        "first_release": "2019",
        "summary": "Framework declarativo de Apple para interfaces en todas sus plataformas.",
        "pros": [
            "Acceso inmediato a las APIs nuevas de Apple",
            "Un mismo código de UI para iPhone, iPad, Mac y Watch",
            "Previews en vivo en Xcode",
        ],
        "cons": ["Solo ecosistema Apple", "Algunas funciones nuevas exigen versiones recientes de iOS"],
        "use_when": "La app es solo para dispositivos Apple o se necesita la máxima calidad nativa.",
    },
    {
        "slug": "flutter",
        "name": "Flutter",
        "type": "multiplataforma",
        "company": "Google",
        "language": "Dart",
        "platforms": ["Android", "iOS", "Web", "Windows", "macOS", "Linux"],
        "first_release": "2018 (1.0)",
        "summary": (
            "SDK que dibuja su propia interfaz con un motor gráfico, de modo que la app "
            "se ve igual en todas las plataformas a partir de un único código en Dart."
        ),
        "pros": [
            "Un solo código para Android e iOS",
            "Hot reload: los cambios se ven al instante",
            "Interfaz consistente y gran catálogo de paquetes en pub.dev",
        ],
        "cons": [
            "Hay que aprender Dart",
            "Binarios algo más pesados que los nativos",
            "Las APIs nativas muy nuevas pueden requerir plugins propios",
        ],
        "use_when": "Equipo pequeño que necesita Android + iOS con una UI personalizada.",
    },
    {
        "slug": "react-native",
        "name": "React Native",
        "type": "multiplataforma",
        "company": "Meta",
        "language": "JavaScript / TypeScript",
        "platforms": ["Android", "iOS"],
        "first_release": "2015",
        "summary": (
            "Permite escribir apps con React que se renderizan con componentes nativos reales. "
            "Expo es el entorno recomendado para empezar y para compilar en la nube."
        ),
        "pros": [
            "Aprovecha conocimientos de React y del ecosistema npm",
            "Componentes nativos reales",
            "Actualizaciones OTA del código JavaScript (por ejemplo, EAS Update)",
        ],
        "cons": ["Dependencias nativas que pueden romperse al actualizar", "Depurar puede ser más complejo"],
        "use_when": "El equipo ya trabaja con React/TypeScript en la web.",
    },
    {
        "slug": "kotlin-multiplatform",
        "name": "Kotlin Multiplatform (KMP)",
        "type": "multiplataforma",
        "company": "JetBrains",
        "language": "Kotlin",
        "platforms": ["Android", "iOS", "Web", "Escritorio", "Servidor"],
        "first_release": "2023 (versión estable)",
        "summary": (
            "Comparte la lógica de negocio (red, datos, validaciones) entre plataformas y deja "
            "que cada una tenga UI nativa, o comparte también la UI con Compose Multiplatform."
        ),
        "pros": [
            "Se puede adoptar de forma gradual en apps existentes",
            "La UI puede seguir siendo 100 % nativa",
            "Respaldo de Google para compartir lógica entre Android e iOS",
        ],
        "cons": ["Ecosistema de librerías más pequeño", "El equipo iOS debe integrarse con código Kotlin"],
        "use_when": "Ya hay una app Android en Kotlin y se quiere reutilizar la lógica en iOS.",
    },
    {
        "slug": "dotnet-maui",
        "name": ".NET MAUI",
        "type": "multiplataforma",
        "company": "Microsoft",
        "language": "C#",
        "platforms": ["Android", "iOS", "Windows", "macOS"],
        "first_release": "2022",
        "summary": "Sucesor de Xamarin.Forms para crear apps nativas con C# y XAML.",
        "pros": ["Ideal para equipos .NET", "Comparte código con backends en C#"],
        "cons": ["Comunidad más pequeña en móvil", "Xamarin ya no tiene soporte (migrar a MAUI)"],
        "use_when": "La organización trabaja con .NET y Azure.",
    },
    {
        "slug": "ionic-capacitor",
        "name": "Ionic + Capacitor",
        "type": "híbrido",
        "company": "Ionic",
        "language": "HTML / CSS / JavaScript (Angular, React o Vue)",
        "platforms": ["Android", "iOS", "Web (PWA)"],
        "first_release": "2013 (Ionic) / 2019 (Capacitor)",
        "summary": (
            "La app es una aplicación web que corre dentro de un WebView nativo; "
            "Capacitor da acceso a cámara, GPS, notificaciones y otras APIs del dispositivo."
        ),
        "pros": ["Reutiliza directamente código web existente", "Un mismo código para web, Android e iOS"],
        "cons": ["Rendimiento inferior en animaciones o listas muy pesadas", "Aspecto menos nativo"],
        "use_when": "Ya existe una web y se necesita una app en tiendas con poco esfuerzo.",
    },
]

ARTICLES = [
    {
        "slug": "nativo-vs-multiplataforma",
        "title": "Nativo, multiplataforma o híbrido: cómo elegir",
        "category": "fundamentos",
        "level": "básico",
        "tags": ["arquitectura", "frameworks", "decisión"],
        "summary": "Criterios para decidir con qué tecnología construir una app móvil.",
        "content": (
            "Nativo (Kotlin/Compose en Android, Swift/SwiftUI en iOS): mejor rendimiento y acceso "
            "inmediato a las APIs del sistema, pero hay que mantener dos códigos y dos equipos.\n\n"
            "Multiplataforma (Flutter, React Native, KMP): un solo código para ambas plataformas. "
            "Reduce costos y tiempo; hoy cubre la gran mayoría de casos de negocio.\n\n"
            "Híbrido (Ionic/Capacitor): una web empaquetada en un WebView. Es lo más rápido si ya "
            "existe una web, aunque con menor rendimiento en interfaces exigentes.\n\n"
            "Preguntas clave: ¿qué sabe hacer el equipo? ¿la app usa mucho hardware (AR, Bluetooth, "
            "audio en tiempo real)? ¿cuál es el presupuesto y el plazo? ¿se necesita también versión web?"
        ),
    },
    {
        "slug": "ciclo-de-vida-app",
        "title": "Ciclo de vida de una aplicación móvil",
        "category": "fundamentos",
        "level": "básico",
        "tags": ["lifecycle", "android", "ios"],
        "summary": "Estados por los que pasa una app y por qué importan.",
        "content": (
            "El sistema operativo puede pausar, detener o cerrar una app en cualquier momento para "
            "liberar memoria. En Android, las Activities pasan por onCreate, onStart, onResume, "
            "onPause, onStop y onDestroy; en iOS la app pasa por los estados active, inactive, "
            "background y suspended.\n\n"
            "Buenas prácticas: guardar el estado del usuario cuando la app pasa a segundo plano, "
            "liberar recursos (cámara, GPS) al pausar y no asumir que la app seguirá en memoria. "
            "Usar ViewModel en Android y el manejo de escenas en iOS ayuda a sobrevivir rotaciones y cierres."
        ),
    },
    {
        "slug": "arquitectura-mvvm-clean",
        "title": "Arquitectura recomendada: MVVM y capas limpias",
        "category": "arquitectura",
        "level": "intermedio",
        "tags": ["mvvm", "clean architecture", "estado"],
        "summary": "Cómo organizar el código para que sea mantenible y fácil de probar.",
        "content": (
            "El patrón más extendido es MVVM con flujo de datos unidireccional: la Vista solo "
            "muestra el estado y envía eventos; el ViewModel transforma los eventos en un nuevo "
            "estado; los Repositorios obtienen los datos de la red o de la base de datos local.\n\n"
            "Capas típicas: UI (pantallas) → dominio (casos de uso, reglas de negocio) → datos "
            "(repositorios, API, almacenamiento). La inyección de dependencias (Hilt/Koin en "
            "Android, inicializadores o factories en Swift) permite reemplazar piezas en las pruebas."
        ),
    },
    {
        "slug": "autenticacion-movil",
        "title": "Autenticación segura en apps móviles",
        "category": "seguridad",
        "level": "intermedio",
        "tags": ["login", "oauth", "pkce", "tokens", "biometría"],
        "summary": "Cómo implementar login en una app móvil conectada a un backend como este.",
        "content": (
            "Una app móvil no debe guardar contraseñas. El flujo recomendado es: la app envía las "
            "credenciales una vez por HTTPS, el backend responde con un access token de vida corta "
            "y un refresh token, y la app los guarda en almacenamiento seguro (Keychain en iOS, "
            "Android Keystore / EncryptedSharedPreferences o DataStore cifrado en Android).\n\n"
            "Para login social (Google, Apple) se usa OAuth 2.0 con PKCE y el navegador del sistema "
            "(Custom Tabs en Android, ASWebAuthenticationSession en iOS), nunca un WebView propio. "
            "En iOS, si se ofrece login con terceros, Apple suele exigir también 'Sign in with Apple'.\n\n"
            "La biometría (huella, Face ID) sirve para desbloquear el token guardado, no para "
            "reemplazar la autenticación del servidor. Las passkeys son la alternativa moderna a las contraseñas."
        ),
    },
    {
        "slug": "owasp-masvs",
        "title": "Seguridad móvil: OWASP MASVS y riesgos comunes",
        "category": "seguridad",
        "level": "avanzado",
        "tags": ["owasp", "masvs", "seguridad", "cifrado"],
        "summary": "Estándar de referencia para verificar la seguridad de una app móvil.",
        "content": (
            "OWASP MASVS (Mobile Application Security Verification Standard) define controles en "
            "áreas como almacenamiento, criptografía, autenticación, red, plataforma, código, "
            "resiliencia y privacidad. La guía MASTG explica cómo probarlos.\n\n"
            "Riesgos frecuentes: claves de API o secretos dentro del código de la app (se pueden "
            "extraer), datos sensibles en logs o almacenamiento sin cifrar, tráfico HTTP sin TLS, "
            "deep links que no validan sus parámetros y confiar en validaciones hechas solo en el cliente.\n\n"
            "Regla de oro: todo lo que está en el dispositivo puede ser leído o modificado por un "
            "atacante; las decisiones de seguridad deben tomarse en el backend."
        ),
    },
    {
        "slug": "offline-first",
        "title": "Apps offline-first y sincronización",
        "category": "datos",
        "level": "intermedio",
        "tags": ["offline", "sqlite", "room", "sincronización"],
        "summary": "Cómo hacer que la app funcione sin conexión.",
        "content": (
            "En móvil la conexión es intermitente. Una app offline-first guarda los datos en una base "
            "local (Room o SQLite en Android, SwiftData o Core Data en iOS, drift o sqflite en Flutter) "
            "y la interfaz lee siempre de ahí; en segundo plano se sincroniza con el servidor.\n\n"
            "Puntos a resolver: cola de cambios pendientes, reintentos con backoff, resolución de "
            "conflictos (última escritura gana, versión por registro o fusión) y tareas en segundo "
            "plano (WorkManager en Android, BGTaskScheduler en iOS)."
        ),
    },
    {
        "slug": "notificaciones-push",
        "title": "Notificaciones push",
        "category": "integraciones",
        "level": "intermedio",
        "tags": ["push", "fcm", "apns", "engagement"],
        "summary": "Cómo funcionan y cómo usarlas sin molestar al usuario.",
        "content": (
            "Android usa Firebase Cloud Messaging (FCM) y iOS usa Apple Push Notification service "
            "(APNs); FCM también puede enviar a iOS a través de APNs. La app obtiene un token del "
            "dispositivo, lo envía al backend y el backend lo usa para mandar mensajes.\n\n"
            "En iOS y en Android 13 o superior hay que pedir permiso explícito al usuario. Conviene "
            "pedirlo en el momento en que aporta valor, no al abrir la app por primera vez, y "
            "permitir elegir qué tipo de avisos recibir."
        ),
    },
    {
        "slug": "rendimiento",
        "title": "Rendimiento y consumo de batería",
        "category": "calidad",
        "level": "intermedio",
        "tags": ["rendimiento", "batería", "anr", "profiling"],
        "summary": "Métricas clave y herramientas para medir una app rápida.",
        "content": (
            "Métricas importantes: tiempo de arranque en frío, fotogramas por segundo (60 o 120 fps, "
            "sin saltos), uso de memoria, tamaño de la app, tasa de cierres inesperados (crash-free "
            "users) y ANR en Android (app que no responde durante más de 5 segundos).\n\n"
            "Herramientas: Android Studio Profiler, Baseline Profiles y Macrobenchmark en Android; "
            "Instruments en Xcode; Firebase Performance y Crashlytics en producción.\n\n"
            "Consejos: no bloquear el hilo principal con red o disco, paginar listas largas, "
            "comprimir y cachear imágenes y agrupar las peticiones de red."
        ),
    },
    {
        "slug": "pruebas-moviles",
        "title": "Estrategia de pruebas en móvil",
        "category": "calidad",
        "level": "intermedio",
        "tags": ["testing", "ci", "qa"],
        "summary": "Pirámide de pruebas aplicada a apps móviles.",
        "content": (
            "Base de la pirámide: pruebas unitarias de ViewModels y casos de uso (JUnit, XCTest o "
            "Swift Testing, flutter_test). En el medio, pruebas de UI (Compose testing, Espresso, "
            "XCUITest). Arriba, pocas pruebas end-to-end en dispositivos reales (Maestro, Appium, "
            "Detox) o en granjas como Firebase Test Lab.\n\n"
            "Automatiza compilación, pruebas y firma con CI/CD (GitHub Actions, Bitrise, Codemagic, "
            "fastlane) y distribuye betas con TestFlight y las pistas de prueba de Google Play."
        ),
    },
    {
        "slug": "publicacion-tiendas",
        "title": "Publicar en Google Play y App Store",
        "category": "publicación",
        "level": "básico",
        "tags": ["google play", "app store", "release", "firma"],
        "summary": "Pasos y requisitos para llevar una app a las tiendas.",
        "content": (
            "Google Play: crear la cuenta en Play Console, firmar la app (Play App Signing), subir un "
            "AAB, completar la ficha, la clasificación de contenido y el formulario de seguridad de "
            "datos. Las cuentas personales nuevas deben hacer una prueba cerrada con testers antes de "
            "publicar en producción.\n\n"
            "App Store: inscribirse en el Apple Developer Program, crear la app en App Store Connect, "
            "subir la compilación desde Xcode, completar las etiquetas de privacidad y enviar a revisión.\n\n"
            "En ambas tiendas se necesita una política de privacidad pública y, si la app permite "
            "crear cuentas, una forma de eliminar la cuenta desde la app."
        ),
    },
    {
        "slug": "accesibilidad",
        "title": "Accesibilidad en apps móviles",
        "category": "diseño",
        "level": "básico",
        "tags": ["accesibilidad", "talkback", "voiceover", "ux"],
        "summary": "Hacer la app usable para todas las personas.",
        "content": (
            "Probar con los lectores de pantalla TalkBack (Android) y VoiceOver (iOS). Dar etiquetas "
            "a botones con iconos, respetar el tamaño de texto que configure el usuario, mantener un "
            "contraste suficiente (WCAG AA: 4.5:1 para texto normal) y áreas táctiles de al menos "
            "48 dp en Android o 44 pt en iOS.\n\n"
            "Guías de diseño de referencia: Material Design 3 (Android) y Human Interface Guidelines (Apple)."
        ),
    },
    {
        "slug": "monetizacion",
        "title": "Modelos de monetización",
        "category": "negocio",
        "level": "básico",
        "tags": ["suscripciones", "compras in-app", "anuncios"],
        "summary": "Formas habituales de generar ingresos con una app.",
        "content": (
            "Modelos: pago único, freemium con compras in-app, suscripciones, publicidad (AdMob y "
            "otras redes) o app gratuita como canal de un negocio existente.\n\n"
            "Los bienes digitales vendidos dentro de la app suelen tener que pasar por el sistema de "
            "pagos de cada tienda, con comisiones de entre el 15 % y el 30 %. Las reglas cambian según "
            "el país por nuevas regulaciones (por ejemplo, en la Unión Europea y EE. UU.), así que "
            "conviene revisar las condiciones vigentes antes de diseñar el modelo de pagos."
        ),
    },
]

GLOSSARY = [
    ("aab", "AAB (Android App Bundle)", "Formato de publicación en Google Play; la tienda genera APKs optimizados para cada dispositivo."),
    ("apk", "APK", "Paquete instalable de Android. Se usa para instalación directa y pruebas."),
    ("ipa", "IPA", "Paquete de una app iOS, firmado para su distribución."),
    ("sdk", "SDK", "Kit de desarrollo de software: librerías y herramientas para crear apps en una plataforma."),
    ("api-level", "Nivel de API (minSdk / targetSdk)", "Número que identifica cada versión de Android. minSdk es la mínima soportada y targetSdk aquella para la que se optimizó la app."),
    ("anr", "ANR", "Application Not Responding: Android avisa cuando el hilo principal queda bloqueado durante unos 5 segundos."),
    ("deep-link", "Deep link", "Enlace que abre una pantalla concreta de la app. Las versiones verificadas son App Links (Android) y Universal Links (iOS)."),
    ("fcm", "FCM", "Firebase Cloud Messaging: servicio de Google para enviar notificaciones push."),
    ("apns", "APNs", "Apple Push Notification service: servicio de Apple para enviar notificaciones push a sus dispositivos."),
    ("pkce", "PKCE", "Extensión de OAuth 2.0 que protege el flujo de autorización en apps públicas como las móviles."),
    ("keychain", "Keychain", "Almacén seguro de iOS para contraseñas, tokens y claves."),
    ("keystore", "Android Keystore", "Sistema de Android para guardar claves criptográficas protegidas por hardware cuando está disponible."),
    ("hot-reload", "Hot reload", "Aplicar cambios de código a la app en ejecución sin perder su estado (Flutter, React Native, Compose)."),
    ("ota", "Actualización OTA", "Over-the-air: actualizar parte de la app (por ejemplo, el JavaScript en React Native) sin pasar por la tienda, dentro de lo que permiten sus políticas."),
    ("testflight", "TestFlight", "Servicio de Apple para distribuir versiones beta de apps iOS a testers."),
    ("r8", "R8 / ProGuard", "Herramientas que reducen, optimizan y ofuscan el código de una app Android."),
    ("code-signing", "Firma de código", "Proceso que garantiza el autor de la app y que no fue modificada. Es obligatorio en ambas plataformas."),
    ("webview", "WebView", "Componente que muestra contenido web dentro de una app nativa; es la base de las apps híbridas."),
    ("pwa", "PWA", "Progressive Web App: web instalable con soporte offline, a medio camino entre una web y una app."),
    ("mvvm", "MVVM", "Model-View-ViewModel: patrón de arquitectura que separa la interfaz de la lógica de presentación."),
    ("runtime-permissions", "Permisos en tiempo de ejecución", "Permisos sensibles (cámara, ubicación, notificaciones) que el usuario concede mientras usa la app, no al instalarla."),
    ("passkey", "Passkey", "Credencial basada en FIDO2/WebAuthn que reemplaza la contraseña y se desbloquea con biometría o el PIN del dispositivo."),
]
