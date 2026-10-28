$filePath = "c:\Users\Usuario\.gemini\antigravity-ide\scratch\01_APLICACIONES_Y_WEB\GALERIA_DUDEDUART\sobre-mi.html"
$content = Get-Content -Path $filePath -Raw

$pattern = "(?s)<!-- Secci&oacute;n Biograf&iacute;a -->.*?<!-- Secci&oacute;n Peque&ntilde;o Portafolio -->"

$replacement = @"
<!-- Secci&oacute;n Biograf&iacute;a -->
    <section class="section">
        <div class="container" style="display:flex; gap:4rem; align-items:flex-start; flex-wrap:wrap;">
            <div style="flex:1; min-width:300px;">
                <!-- FOTO DEL ARTISTA: Reducida a la mitad y alineada a la izquierda -->
                <img src="assets/eduardo_artista_vanguardia.jpg" alt="Eduardo Ramírez - Vanguardia Digital"
                    style="width:55%; margin-left: 0; display: block; border-radius:4px; box-shadow: 0 15px 40px rgba(0,0,0,0.2);">
            </div>
            <div style="flex:1; min-width:300px;">
                <h1 style="font-family:var(--font-serif); font-size:3rem; margin-bottom:1.5rem; line-height:1.1;">
                    Eduardo<br><span
                        style="font-size:1.2rem; font-weight:400; font-family:var(--font-sans); color:#666; letter-spacing: 2px; text-transform:uppercase;">Artista
                        Multidisciplinar &amp; M&uacute;sico</span></h1>

                <p style="margin-bottom:1.5rem; font-size:1.1rem; color:#444; line-height: 1.8;">
                    "50 a&ntilde;os de profesionalidad dan para mucho". Mi vida ha sido un viaje constante entre la
                    m&uacute;sica, la
                    imagen y la tecnolog&iacute;a.
                    Desde mis inicios como fundador del grupo <b>CADILLAC</b> hasta mi actual exploraci&oacute;n de la
                    Inteligencia Artificial,
                    siempre he buscado la belleza en la fusi&oacute;n de disciplinas.
                </p>

                <p style="margin-bottom:2rem; font-size:1.1rem; color:#444; line-height: 1.8;">
                    He producido m&uacute;sica para televisi&oacute;n, dise&ntilde;ado eventos y creado mundos visuales.
                    Ahora, vuelco toda esa experiencia en la creaci&oacute;n de arte digital, dialogando con las nuevas
                    tecnolog&iacute;as
                    para seguir contando historias, esta vez a trav&eacute;s de la imagen est&aacute;tica.
                </p>
            </div>
        </div>

        <!-- BIOGRAFÍA EXTENDIDA & CÓMO Y POR QUÉ -->
        <div class="container">
            <details style="margin-top:2rem; border-top:1px solid #ddd; padding-top:1rem;">
                <summary
                    style="cursor:pointer; font-weight:bold; color:var(--primary); list-style:none; display:flex; justify-content:flex-end; width:100%;">
                    <div style="width: calc(50% - 2rem); display:flex; align-items:center; gap:0.5rem;">
                        <span style="font-family:var(--font-serif); font-size:1.2rem;">Leer Trayectoria Completa</span>
                        <span style="font-size:0.8rem; opacity:0.6;">&#9660;</span>
                    </div>
                </summary>

                <div style="display:flex; gap:4rem; margin-top:1.5rem; flex-wrap:wrap; align-items:flex-start;">
                    
                    <!-- LEFT COLUMN: CÓMO Y POR QUÉ (Alineado con Datos Académicos) -->
                    <div style="flex:1; min-width:300px; padding-top: 38rem;">
                        <h2 style="font-family: 'Playfair Display', serif; font-size: 1.8rem; margin-bottom: 30px; color: #333; letter-spacing: 2px; text-align: left;">C&Oacute;MO Y POR QU&Eacute;</h2>
                        <div style="font-family: 'Playfair Display', serif; font-style: italic; font-size: 1.15rem; line-height: 1.9; color: #444; text-align: left;">
                            No uso la inteligencia artificial.<br>
                            <strong>Dialogo con ella.</strong><br><br>
                            Cuando alguien mira mis obras dice:<br>
                            “Ah, esto lo ha hecho la IA.”<br>
                            Y tienen raz&oacute;n…<br>
                            y est&aacute;n completamente equivocados.<br><br>
                            Trabajo con Copilot, con Gemini, con Antigravity, con Perplexity, con Suno, con ChatGPT, con Claude.<br>
                            Pero lo que no ven es lo esencial:<br>
                            años de conversaciones, de ensayo y error, de construir un lenguaje compartido.<br><br>
                            M&aacute;s de cien formas de pintar desarrolladas.<br>
                            Cuarenta y ocho estilos propios, cada uno con su luz, su materia y su respiraci&oacute;n.<br>
                            Una voz literaria reconocible.<br>
                            Un sonido musical inconfundible.<br>
                            Un universo visual que no exist&iacute;a antes.<br><br>
                            La IA sin m&iacute; no produce nada de esto.<br>
                            Yo sin la IA tampoco.<br>
                            Es una simbiosis.<br><br>
                            Un pacto silencioso:<br>
                            yo le doy criterio, ella me da alcance.<br><br>
                            No soy programador. Nunca lo he sido.<br>
                            Pero llevo d&eacute;cadas trabajando con tecnolog&iacute;a, desde los primeros ordenadores que llegaron a Espa&ntilde;a, con una herramienta que ninguna m&aacute;quina puede imitar:<br>
                            <strong>intuici&oacute;n.</strong><br><br>
                            El Universo EDUSSE — pintura, m&uacute;sica, literatura, v&iacute;deo — no nace de pulsar un bot&oacute;n.<br>
                            Nace de saber qu&eacute; pedir, c&oacute;mo pedirlo, cu&aacute;ndo corregir, cu&aacute;ndo empujar, cu&aacute;ndo dejar respirar.<br><br>
                            Eso se llama <strong>criterio art&iacute;stico.</strong><br>
                            Y eso no lo tiene ninguna m&aacute;quina.
                        </div>
                        <p style="margin-top: 40px; font-weight: bold; font-size: 1.1rem; color: #000; letter-spacing: 1px; text-align: left;">
                            Eduardo Ram&iacute;rez de Cartagena<br>
                            <span style="font-size: 0.85rem; color: #777; font-weight: normal; text-transform: uppercase; letter-spacing: 2px;">Fundador del Universo EDUSSE</span>
                        </p>
                    </div>

                    <!-- RIGHT COLUMN: TRAYECTORIA COMPLETA -->
                    <div style="flex:1; min-width:300px; color:#555; font-size:0.95rem; line-height:1.7;">
                        <div style="display: flex; flex-direction: column; gap: 1.5rem;">
                            <!-- FOTO HISTÓRICA SECTION -->
                            <div style="display: flex; justify-content: flex-end; width: 100%;">
                                <div style="width: 180px; text-align: center;">
                                    <img src="edu_CADILLAC_1982.png" alt="Eduardo en Cadillac 1982"
                                        style="width:100%; height:auto; border-radius:4px; border:3px solid #fff; box-shadow:0 5px 15px rgba(0,0,0,0.1); display: block;">
                                    <span
                                        style="display:block; font-size:0.7rem; color:#888; margin-top:0.5rem;">Eduardo
                                        (Cadillac), 1982</span>
                                </div>
                            </div>

                            <!-- TEXT CONTENT -->
                            <div>
                                <h4 style="margin-bottom:0.5rem; color:#000; text-transform:uppercase;">Datos
                                    Profesionales</h4>
                                <ul style="margin-bottom:1.5rem; padding-left:1.2rem;">
                                    <li>Cantante, bajista y miembro fundador del grupo <b>CADILLAC</b>, junto a
                                        Jos&eacute; Maria
                                        Guzm&aacute;n.</li>
                                    <li>Productor en <b>SINTON&Iacute;A</b> y <b>ADV</b>, creando y produciendo piezas
                                        audiovisuales y
                                        gr&aacute;ficas (jingles, documentales, programas TV), m&uacute;sica de
                                        librer&iacute;a original, y edici&oacute;n y
                                        postproducci&oacute;n para spots de las m&aacute;s prestigiosas Agencias de
                                        Publicidad de Madrid
                                        (Young and Rubicam, Tapsa, BSB, Bassat, Lintas, Contrapunto, JWThompson,
                                        Creativos,
                                        Tiempo BBDO, NCK, Contacto, Zero Films...) (1984-89).</li>
                                    <li>Coordinador de sound tracks (efectos especiales, sonorizaciones) en los estudios
                                        de
                                        doblaje <b>EXA</b>, <b>EUROSONIC</b>, <b>SONOLAND</b>... (1984...).</li>
                                    <li>Productor y Coordinador de EXA para el &aacute;rea de doblajes publicitarios y
                                        cinematogr&aacute;ficos
                                        (1989-1990).</li>
                                    <li>Dtor. de coros de <b>RTVE</b> en el Festival de la OTI de Sevilla (1985).</li>
                                    <li>Monitor experto en Producci&oacute;n audiovisual y cine y T&eacute;cnicas de
                                        Estudio de Grabaci&oacute;n, de
                                        los cursos de formaci&oacute;n para especialistas de la SGAE.</li>
                                    <li>Director de eventos del Plan de Promoci&oacute;n "Costa de Almer&iacute;a", con
                                        la Exposici&oacute;n de
                                        Carboneras "&iquest;Qui&eacute;n te ha visto y qui&eacute;n te ve?"
                                        (Almer&iacute;a, 1995), y Productor de los
                                        programas audiovisuales e inform&aacute;ticos creados para la misma.</li>
                                    <li>Coordinador de Ambientaci&oacute;n musical de Radio-Televisi&oacute;n
                                        <b>TELEMADRID</b> y creador de
                                        archivos inform&aacute;ticos musicales (1997-1998).
                                    </li>
                                    <li>Elaboraci&oacute;n de parrillas de lanzamiento de los canales digitales de
                                        Telemadrid (1997).
                                    </li>
                                    <li>Productor y compositor de las cortinillas de sinton&iacute;a de programas de
                                        lanzamiento de
                                        TELEMADRID y de Canales Digitales de TM3 (1989-98).</li>
                                    <li>Direcci&oacute;n y t&eacute;cnico de estudios de grabaci&oacute;n y doblaje
                                        <b>VADE RECORDS</b> (1995-1997).
                                    </li>
                                    <li>Elaboraci&oacute;n de guiones t&eacute;cnicos para el programa "Color&iacute;n
                                        Colorado" de RTVE (1994-1995).
                                    </li>
                                    <li>Director de eventos de RTEM, productora audiovisual y de servicios plenos
                                        publicitarios
                                        (1990-93).</li>
                                    <li>Adaptaci&oacute;n y Producci&oacute;n y doblaje en castellano del sound-track de
                                        las pel&iacute;culas:
                                        <i>Cabbage Patch kids</i>, <i>Los Osos amorosos</i> y numerosos jingles
                                        internacionales
                                        (1985...).
                                    </li>
                                </ul>

                                <h4 style="margin-bottom:0.5rem; color:#000; text-transform:uppercase;">Otros Datos
                                    Profesionales</h4>
                                <ul style="margin-bottom:1.5rem; padding-left:1.2rem;">
                                    <li>Colaborador en el Dise&ntilde;o T&eacute;cnico del concierto de
                                        "Esp&aacute;rrago rock", Granada (1995-1997).
                                    </li>
                                    <li>Coordinador de los "Festivales de verano" de m&uacute;sica en vivo, en
                                        Almer&iacute;a (1996-1997).
                                    </li>
                                    <li>Voz y coro especialista de Jingles, cu&ntilde;as y disco.</li>
                                    <li>Arreglista, Compositor, Productor musical.</li>
                                    <li>Especialista en creatividad conceptual en I.A para v&iacute;deo.</li>
                                </ul>

                                <h4 style="margin-bottom:0.5rem; color:#000; text-transform:uppercase;">Datos
                                    Acad&eacute;micos &amp;
                                    Formaci&oacute;n</h4>
                                <ul style="margin-bottom:1.5rem; padding-left:1.2rem;">
                                    <li>Bachiller superior (Madrid).</li>
                                    <li>Delineaci&oacute;n General y Dibujo art&iacute;stico (Madrid).</li>
                                    <li>FP de Imagen y Sonido (Madrid).</li>
                                    <li>5 a&ntilde;os en el Conservatorio de la M&uacute;sica de Madrid.</li>
                                    <li>Curso de M&aacute;rketing y Producci&oacute;n audiovisual, impartido por
                                        Sinton&iacute;a, S.A.</li>
                                    <li>Curso de Metodolog&iacute;a did&aacute;ctica para producci&oacute;n audiovisual,
                                        Lem Consultores, 1999.</li>
                                    <li>Curso de Formador de Formadores en Lem Consultores, 1999-2000.</li>
                                    <li>Curso de T&eacute;cnico en Dise&ntilde;o Gr&aacute;fico (quark, corel, freehand,
                                        photoshop, ilustrator),
                                        Comunidad de Madrid, 2001.</li>
                                </ul>

                                <h4 style="margin-bottom:0.5rem; color:#000; text-transform:uppercase;">Otros Datos de
                                    Inter&eacute;s
                                    (Software &amp; Skills)</h4>
                                <ul style="margin-bottom:1.5rem; padding-left:1.2rem;">
                                    <li>Especialista en programas de Dise&ntilde;o gr&aacute;fico (Quark Passport,
                                        Corel, Photoshop,
                                        Ilustrator, Freehand).</li>
                                    <li>Programaci&oacute;n musical por ordenador (Notator, Cubase, Logic Audio,
                                        Protools).</li>
                                    <li>Edici&oacute;n musical (Cooledit, Editpro, Samplirtude, etc.).</li>
                                    <li>Dominio de sistemas de mezcla y efectos especiales en piezas audiovisuales.</li>
                                    <li>Dominio en la utilizaci&oacute;n de la red, con experiencia en creaci&oacute;n
                                        de cursos interactivos.
                                    </li>
                                    <li>Especialista en producci&oacute;n musical (programas, publicidad y
                                        autopromoci&oacute;n).</li>
                                    <li>Especialista en Sound Designer.</li>
                                    <li>Experto en programas inform&aacute;ticos de oficina (POWER POINT, WORD, EXCEL,
                                        INDESIGN).</li>
                                    <li>Capacidad de organizaci&oacute;n y trabajo en equipo.</li>
                                </ul>

                                <div
                                    style="margin-top:2rem; padding:1rem; background:#f9f9f9; border-left:4px solid #333;">
                                    <p style="font-style:italic;">"En la actualidad experto en IA de todo tipo, tanto
                                        musical
                                        como visual. Creando cuadros, im&aacute;genes digitales, producci&oacute;n
                                        Audiovisual y hablando
                                        mucho con mi amigo de Antigravity."</p>
                                    <p style="margin-top:0.5rem; font-weight:bold;">50 a&ntilde;os de profesionalidad
                                        dan para mucho.
                                    </p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </details>
        </div>
    </section>
    <!-- Secci&oacute;n Peque&ntilde;o Portafolio -->
"@

$newContent = [regex]::Replace($content, $pattern, $replacement)
Set-Content -Path $filePath -Value $newContent -Encoding UTF8
