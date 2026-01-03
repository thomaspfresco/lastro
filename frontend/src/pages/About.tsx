import { useContentReady } from "../composables/usePageTransition";
import logoSvg from "../assets/logo.svg";

interface ProjectBlockProps {
  title: string;
  projects: Projects;
  topOffset?: number;
}

const About: React.FC<ProjectBlockProps> = ({
  topOffset = 0,
}) => {
  useContentReady(true);

  return <div className="grid-setup">
    <div className="grid grid-cols-1 md:grid-cols-[1fr_2fr] gap-0 md:gap-6 lg:gap-8">
      <div>
        <div className="sticky bg-color-bg z-10 pt-px pb-3"
          style={{ top: `calc(var(--menu-height) + ${topOffset}px)` }}>
            <h2 className="text-title-2 mb-3">Contactos</h2>
          <span className="block h-px w-full bg-color-1 opacity-50" />
        </div>
        <div className="flex flex-col justify-between min-h-[calc(100%-var(--menu-height))] gap-3">
          <div className="flex flex-col">
            <a href="mailto:amusicaportuguesa@gmail.com" target="_blank">amusicaportuguesa@gmail.com</a>
            <a href="https://amusicaportuguesaagostardelapropria.org/" target="_blank">Website</a>
            <a href="https://vimeo.com/mpagdp" target="_blank">Vimeo</a>
            <a href="https://www.facebook.com/amusicaportuguesaagostardelapropria" target="_blank">Facebook</a>
            <a href="https://www.instagram.com/mpagdp/" target="_blank">Instagram</a>
            <a href="https://www.tiktok.com/@mpagdp.official" target="_blank">TikTok</a>
            <a href="https://linktr.ee/mpagdp" target="_blank">Mais</a>
          </div>
          <div className="flex flex-col justify-start gap-3">
            <img
              src={logoSvg}
              alt="Loading"
              className={`relative z-10 w-10 h-10 transition-opacity duration-500`}
            />
            <p>Com ❤︎ por <a href="" target="_blank">Thomas Fresco</a> e <a href="" target="_blank">Fábio Gouveia</a>.</p>
          </div>
        </div>
      </div>
      <div className="flex flex-col">
        <div className="mb-24">
          <div className="sticky bg-color-bg z-10 pt-px pb-3"
          style={{ top: `calc(var(--menu-height) + ${topOffset}px)` }}>
            <h2 className="text-title-2 mb-3">Lastro</h2>
            <span className="block h-px w-full bg-color-1 opacity-50" />
          </div>
          <div className="flex flex-col">
            <p>A Música Portuguesa a Gostar Dela Própria é um projeto de arquivo vivo e celebração da identidade sonora de Portugal. Desde 2011, percorre o país de norte a sul, ilhas incluídas, registando — em vídeo, som e palavra — músicos, cantores, poetas, tocadores e comunidades que mantêm viva a alma da música portuguesa.</p>
            <p>Mais do que um arquivo, é um retrato coletivo. Sem estúdios, sem filtros e sem artifícios, cada gravação acontece no lugar de origem — na aldeia, na rua, na cozinha, na serra ou à beira-mar —, deixando que o som e o silêncio do espaço façam parte da canção.</p>
            <p>O projeto nasceu da vontade de Tiago Pereira de mostrar a força da tradição e a sua constante reinvenção. O resultado é um mosaico de vozes e expressões que atravessa géneros e gerações — do fado à música popular, do canto alentejano à eletrónica, da tradição oral à experimentação.</p>
            <p>A Música Portuguesa a  Gostar Dela Própria é, acima de tudo, um gesto de escuta. Um país a ouvir-se a si próprio.</p>
          </div>
        </div>
        <div className="mb-24">
          <div className="sticky bg-color-bg z-10 pt-px pb-3"
          style={{ top: `calc(var(--menu-height) + ${topOffset}px)` }}>
            <h2 className="text-title-2 mb-3">Música Portuguesa a Gostar Dela Próprio</h2>
            <span className="block h-px w-full bg-color-1 opacity-50" />
          </div>
          <div className="flex flex-col">
            <p>A Música Portuguesa a Gostar Dela Própria é um projeto de arquivo vivo e celebração da identidade sonora de Portugal. Desde 2011, percorre o país de norte a sul, ilhas incluídas, registando — em vídeo, som e palavra — músicos, cantores, poetas, tocadores e comunidades que mantêm viva a alma da música portuguesa.</p>
            <p>Mais do que um arquivo, é um retrato coletivo. Sem estúdios, sem filtros e sem artifícios, cada gravação acontece no lugar de origem — na aldeia, na rua, na cozinha, na serra ou à beira-mar —, deixando que o som e o silêncio do espaço façam parte da canção.</p>
            <p>O projeto nasceu da vontade de Tiago Pereira de mostrar a força da tradição e a sua constante reinvenção. O resultado é um mosaico de vozes e expressões que atravessa géneros e gerações — do fado à música popular, do canto alentejano à eletrónica, da tradição oral à experimentação.</p>
            <p>A Música Portuguesa a  Gostar Dela Própria é, acima de tudo, um gesto de escuta. Um país a ouvir-se a si próprio.</p>
          </div>
        </div>
      </div>
    </div>
  </div>;
};

export default About;
