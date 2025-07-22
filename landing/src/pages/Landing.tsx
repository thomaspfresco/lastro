import { useEffect, useRef, useState } from "react";
import Player from "@vimeo/player";

import logoWhite from "../assets/images/ampagdpbranco.png";
import Definitions from "../components/Definitions";

const videos = [
  "1057209428",
  "1058963839",
  "1057215851",
  "1059300813",
  "1059300839",
  "1059301930",
  "1057486570",
  "1059766720",
  "1058950174",
  "1058950084",
  "1058949961",
  "1058950017",
  "1057495827",
  "1057519241",
  "1059422654",
  "1059422690",
  "1059422724",
  "1058188598",
  "1058224308",
  "1058288083",
  "1058557858",
  "1059168478",
  "1059883934",
  "1060412527",
  "1059884010",
  "1060415324",
  "1061980365",
  "1061344022",
  "1061839046",
  "1061794793",
  "1061986781",
  "1062063459",
  "1062110941",
  "1062732413",
  "1063247895",
  "1063614476",
  "1063815732",
  "1066323575",
  "1066324683",
  "1066324931",
  "1066361218",
  "1066696988",
  "1069740951",
  "1069742086",
  "1070761461",
  "1070772246",
  "1070779447",
  "1070780866",
  "1072822956",
  "1074242008",
  "1075679040",
  "1075680047",
  "1079004371",
  "1079902433",
  "1080101575",
  "1080101825",
  "1080102014",
  "1080102227",
  "1080102307",
  "1080101748",
  "1080102394",
  "1080122899",
  "1080144124",
  "1080771617",
  "1080775395",
  "1080854780",
  "1080854875",
  "1080854948",
  "1085443153",
  "1091815901",
  "1091815961",
  "1091816015",
  "1091816119",
  "1091816305",
  "1091816582",
  "1091816731",
  "1091816791",
  "1091856386",
  "1091856481",
  "1091861380",
  "1091916298",
  "1093054201",
  "1093054267",
  "1093054964",
  "1094647845",
  "1094647993",
  "1094648087",
  "1094648174",
  "1094648293",
  "1094648318",
  "1094668852",
  "1094684377",
  "1094954626",
  "1094954731",
  "1094689537",
  "1094831740",
  "1095680286",
  "1095680397",
  "1095554608",
  "1095680176",
  "1095680537",
  "1059019921",
  "1057095915",
  "1057950863",
];

const Landing = () => {
  const iframeRef = useRef<HTMLIFrameElement>(null);
  const [videoStarted, setVideoStarted] = useState(false);
  const [videoId] = useState(() => {
    const randomIndex = Math.floor(Math.random() * videos.length);
    return videos[randomIndex];
  });

  useEffect(() => {
    if (iframeRef.current) {
      const player = new Player(iframeRef.current);
      player.on("play", () => setVideoStarted(true));
    }
  }, []);

  return (
    <div className="w-screen overflow-hidden">
      {/* LOGO AT BOTTOM */}
      <div className="absolute pt-16 w-full flex justify-center z-[100]">
        <a
          href="https://amusicaportuguesaagostardelapropria.org/"
          target="_blank"
          rel="noopener noreferrer"
          className="cursor-pointer"
        >
          <img
            src={logoWhite}
            alt="Logo"
            className="h-20 w-auto object-contain"
          />
        </a>
      </div>

      {/* SECTION 1 — VIDEO */}
      <div className="relative h-[100dvh] w-full overflow-hidden bg-black">
        {/* Vimeo Background */}
        <div
          className={`absolute inset-0 transition-opacity duration-[2000ms] ease-in-out ${
            videoStarted ? "opacity-50" : "opacity-0"
          }`}
          style={{ zIndex: 0 }}
        >
          <iframe
            ref={iframeRef}
            title="vimeo-background"
            src={`https://player.vimeo.com/video/${videoId}?autoplay=1&loop=1&muted=1&background=1&quality=360p`}
            frameBorder="0"
            allow="autoplay; fullscreen"
            allowFullScreen
            className="absolute top-0 left-1/2 -translate-x-1/2 pointer-events-none"
            style={{
              height: "100vh",
              width: "177.78vh", // maintain 16:9 aspect ratio
              minWidth: "100vw",
              minHeight: "56.25vw",
            }}
          />
        </div>

        {/* Gradient Overlay */}
        <div className="absolute bottom-0 w-full h-[100vh] bg-gradient-to-t from-black to-transparent z-0" />

        {/* Foreground Content */}
        <div className="relative z-10 flex flex-col items-center justify-center h-full text-white text-center px-8 max-w-[1920px] mx-auto">
          <div className="max-w-3xl mx-auto">
            <h1 className="text-5xl font-dela uppercase mb-4">Lastro</h1>
            <Definitions />

            <p className="sm:text-lg md:text-xl mt-12 leading-tight">
              <span className="font-dm_light">O novo motor de busca da </span>
              <a
                href="https://amusicaportuguesaagostardelapropria.org/"
                target="_blank"
                rel="noopener noreferrer"
                className="font-dm_light underline hover:text-[#FA7D00] hover:font-dm_bold"
              >
                Música Portuguesa a Gostar Dela Própria
              </a>
              <span className="font-dm_light"> já está em construção.</span>
            </p>
          </div>

          {/* Animated Scroll Arrow - absolute bottom */}
          <svg
            xmlns="http://www.w3.org/2000/svg"
            className="absolute bottom-14 left-1/2 -translate-x-1/2 h-10 w-10 text-white"
            style={{
              opacity: 0,
              animation: `
                fadeIn 2s ease forwards 7s,
                bounce 2s ease-out infinite
              `,
            }}
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            strokeWidth={1}
            role="img"
            aria-label="Scroll down"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M19 9l-7 7-7-7"
            />
          </svg>
        </div>
      </div>

      {/* SECTION 2 — Footer Section */}
      <div className="min-h-screen bg-black text-white px-8 py-10 flex flex-col justify-center max-w-[1920px] mx-auto">
        <div className="text-left max-w-3xl mx-auto">
          <h2 className="text-base sm:text-lg md:text-3xl font-dela mb-4 md:mb-8">
            Uma nova forma de explorar o património cultural português
          </h2>
          <p className="text-xs sm:text-base md:text-lg leading-normal font-dm_light">
            A plataforma em desenvolvimento permite uma exploração
            interativa do acervo da MPAGDP — simples como conversar com um
            amigo. O resultado de anos de recolha alimenta um motor de
            busca capaz de compreender linguagem natural, ajudando a
            encontrar não só o que procuramos, mas também o que ainda não
            sabemos que queremos ver. A ferramenta promete uma experiência
            acessível e completa, minimizando a sensação de que algo ficou por
            descobrir.
          </p>

          <p className="pt-8 text-xs sm:text-base md:text-2xl leading-normal font-dela">
            Entretanto
          </p>

          {/* Footer Links */}
          <div className="flex flex-wrap gap-x-6 gap-y-1.5 text-sm pt-2 font-dm_bold">
            <a
              href="https://amusicaportuguesaagostardelapropria.org/"
              target="_blank"
              rel="noopener noreferrer"
              className="underline hover:text-[#FA7D00] hover:font-dm_bold break-words"
            >
              Website
            </a>
            <a
              href="https://vimeo.com/mpagdp"
              target="_blank"
              rel="noopener noreferrer"
              className="underline hover:text-[#FA7D00] hover:font-dm_bold break-words"
            >
              Vimeo
            </a>
            <a
              href="https://www.facebook.com/amusicaportuguesaagostardelapropria"
              target="_blank"
              rel="noopener noreferrer"
              className="underline hover:text-[#FA7D00] hover:font-dm_bold break-words"
            >
              Facebook
            </a>
            <a
              href="https://www.instagram.com/mpagdp/"
              target="_blank"
              rel="noopener noreferrer"
              className="underline hover:text-[#FA7D00] hover:font-dm_bold break-words"
            >
              Instagram
            </a>
            <a
              href="https://www.tiktok.com/@mpagdp.official"
              target="_blank"
              rel="noopener noreferrer"
              className="underline hover:text-[#FA7D00] hover:font-dm_bold break-words"
            >
              TikTok
            </a>

            <a
              href="https://linktr.ee/mpagdp"
              target="_blank"
              rel="noopener noreferrer"
              className="underline hover:text-[#FA7D00] hover:font-dm_bold break-words"
            >
              Mais
            </a>
          </div>
        </div>

        {/* LOGO AT BOTTOM */}
        <div className="bg-black pt-6 sm:pt-16 md:pt-20 flex justify-center">
          <img
            src={logoWhite}
            alt="Logo"
            className="h-16 w-auto object-contain"
          />
        </div>

        {/* Bottom Text Section */}
        <div className="flex justify-between items-center max-w-3xl mx-auto w-full border-t border-white/25 pt-6 mt-6 text-white text-xs font-dm_light">
          <div className="text-left max-w-[45%]">
            <p>
              <span>Com ❤︎ por </span>
              <a
                href="https://thomasfresco.pt"
                target="_blank"
                rel="noopener noreferrer"
                className="hover:text-[#FA7D00] hover:font-dm_bold"
              >
                Thomas Fresco
              </a>
              <span>.</span>
            </p>
          </div>
          <div className="text-right max-w-[45%]">
            <p>© 2025 — Todos os direitos reservados.</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Landing;
