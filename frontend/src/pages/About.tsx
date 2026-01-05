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

  return <div className="grid-setup overflow-x-clip">
    <div className="grid grid-cols-1 md:grid-cols-[1fr_2fr] gap-0 md:gap-6 lg:gap-8">
      <div className="sticky order-2 md:order-1 md:h-0 flex flex-col"
        style={{ top: `calc(var(--menu-height) + ${topOffset}px)` }}>
        <div className="bg-color-bg z-20 pt-px pb-3">
          <h2 className="text-title-2 mb-3">Contactos</h2>
          <span className="block h-px w-full bg-color-1 opacity-50" />
        </div>
        <div className="flex flex-col justify-between gap-3 h-full">
          <div className="flex flex-col">
            <a className="cursor-pointer text-color-2 hover:text-color-1 transition-all duration-300"
            href="mailto:amusicaportuguesa@gmail.com" target="_blank">amusicaportuguesa@gmail.com</a>
            <a className="cursor-pointer text-color-2 hover:text-color-1 transition-all duration-300"
            href="https://amusicaportuguesaagostardelapropria.org/" target="_blank">Website</a>
            <a className="cursor-pointer text-color-2 hover:text-color-1 transition-all duration-300"
            href="https://vimeo.com/mpagdp" target="_blank">Vimeo</a>
            <a className="cursor-pointer text-color-2 hover:text-color-1 transition-all duration-300"
            href="https://www.facebook.com/amusicaportuguesaagostardelapropria" target="_blank">Facebook</a>
            <a className="cursor-pointer text-color-2 hover:text-color-1 transition-all duration-300"
            href="https://www.instagram.com/mpagdp/" target="_blank">Instagram</a>
            <a className="cursor-pointer text-color-2 hover:text-color-1 transition-all duration-300"
            href="https://www.tiktok.com/@mpagdp.official" target="_blank">TikTok</a>
            <a className="cursor-pointer text-color-2 hover:text-color-1 transition-all duration-300"
            href="https://linktr.ee/mpagdp" target="_blank">Mais</a>
          </div>
          <div className="flex flex-col justify-start gap-3 mt-12">
            <a href="https://amusicaportuguesaagostardelapropria.org/" target="_blank"><img
              src={logoSvg}
              alt="Loading"
              className={`relative z-10 w-10 h-10 transition-opacity duration-500`}
            /></a>
            <p>Com ❤︎ por <a className="cursor-pointer text-color-2 hover:text-color-1 transition-all duration-300"
            href="https://thomasfresco.pt/" target="_blank">Thomas Fresco</a> e <a className="cursor-pointer text-color-2 hover:text-color-1 transition-all duration-300"
            href="https://fabiogouveia.pt/" target="_blank">Fábio Gouveia</a>.</p>
          </div>
        </div>
      </div>
      <div className="flex flex-col order-1 md:order-2">
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
