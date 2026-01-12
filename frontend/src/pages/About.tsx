import { useContentReady } from "../composables/usePageTransition";
import logoSvg from "../assets/logo.svg";
import lastroImg from "../assets/images/lastro.jpeg";
import curaImg from "../assets/images/cura.jpg";

interface ProjectBlockProps {
  title: string;
  projects: Projects;
}

const About: React.FC<ProjectBlockProps> = () => {
  useContentReady(true);

  return (
    <div className="grid-setup !pt-[var(--menu-height)] overflow-x-clip">
      <div className="grid grid-cols-1 md:grid-cols-[1fr_2fr] gap-0 md:gap-12 lg:gap-16">
        <div
          className="sticky order-2 md:order-1 flex flex-col self-start md:h-[calc(100vh-var(--menu-height)*2-1.5rem)]"
          style={{
            top: "var(--menu-height)",
          }}
        >
          <div className="bg-color-bg z-20 pt-px pb-3">
            <h2 className="text-title-2 my-3">Links Externos</h2>
            <span className="block h-px w-full bg-color-1 opacity-50" />
          </div>
          <div className="flex flex-col justify-between flex-1 min-h-0">
            <div className="flex flex-col gap-2 md:gap-0">
              <a
                className="cursor-pointer text-color-2 hover:text-color-1 transition-all duration-250"
                href="https://amusicaportuguesaagostardelapropria.org/"
                target="_blank"
              >
                Website
              </a>
              <a
                className="cursor-pointer text-color-2 hover:text-color-1 transition-all duration-250"
                href="https://vimeo.com/mpagdp"
                target="_blank"
              >
                Vimeo
              </a>
              <a
                className="cursor-pointer text-color-2 hover:text-color-1 transition-all duration-250"
                href="https://www.facebook.com/amusicaportuguesaagostardelapropria"
                target="_blank"
              >
                Facebook
              </a>
              <a
                className="cursor-pointer text-color-2 hover:text-color-1 transition-all duration-250"
                href="https://www.instagram.com/mpagdp/"
                target="_blank"
              >
                Instagram
              </a>
              <a
                className="cursor-pointer text-color-2 hover:text-color-1 transition-all duration-250"
                href="https://www.tiktok.com/@mpagdp.official"
                target="_blank"
              >
                TikTok
              </a>
              <a
                className="cursor-pointer text-color-2 hover:text-color-1 transition-all duration-250"
                href="https://linktr.ee/mpagdp"
                target="_blank"
              >
                Mais
              </a>
            </div>
            <div className="mt-16">
              <a
                href="https://amusicaportuguesaagostardelapropria.org/"
                target="_blank"
              >
                <img
                  src={logoSvg}
                  alt="Loading"
                  className={`relative z-10 w-10 h-10 mb-4`}
                />
              </a>
              <p className="text-body-2 text-color-2">
                2026. Todos os direitos reservados.
              </p>

              <p className="text-body-2 text-color-2">
                Com ❤︎ por{" "}
                <a
                  className="cursor-pointer text-color-2 hover:text-color-1 transition-all duration-250 underline"
                  href="https://thomasfresco.pt/"
                  target="_blank"
                >
                  Thomas Fresco
                </a>{" "}
                e{" "}
                <a
                  className="cursor-pointer text-color-2 hover:text-color-1 transition-all duration-250 underline"
                  href="https://fabiogouveia.pt/"
                  target="_blank"
                >
                  Fábio Gouveia
                </a>
                .
              </p>
            </div>
          </div>
        </div>
        <div className="flex flex-col order-1 md:order-2">
          <div className="mb-24">
            <div
              className="sticky bg-color-bg z-10 pt-px pb-3"
              style={{ top: "var(--menu-height)" }}
            >
              <h2 className="text-title-2 my-3">Sobre Lastro</h2>
              <span className="block h-px w-full bg-color-1 opacity-50" />
            </div>
            <div className="w-full mb-4 aspect-[5/2] overflow-hidden rounded-lg">
              <img
                src={lastroImg}
                alt="Lastro"
                className="w-full h-full object-cover grayscale"
                style={{ objectPosition: "50% 0%" }}
              />
            </div>
            <div className="flex flex-col gap-3 pr-8">
              <p>
                Uma nova forma de explorar música, tradição oral, memória
                coletiva e património humano.
              </p>
              <p>
                A plataforma permite uma exploração interativa do acervo d'A
                Música Portuguesa A Gostar Dela Própria. O resultado de anos de
                recolha alimenta um motor de busca capaz de compreender
                linguagem natural, ajudando a encontrar não só o que procuramos,
                mas também o que ainda não sabemos que queremos ver. A
                ferramenta promete uma experiência acessível e completa,
                minimizando a sensação de que algo ficou por descobrir — simples
                como conversar com um amigo.
              </p>
            </div>
          </div>
          <div className="mb-12">
            <div
              className="sticky bg-color-bg z-10 pt-px pb-3"
              style={{ top: "var(--menu-height)" }}
            >
              <h2 className="text-title-2 my-3">
                Sobre A Música Portuguesa a Gostar Dela Própria
              </h2>
              <span className="block h-px w-full bg-color-1 opacity-50" />
            </div>
            <div className="w-full mb-4 aspect-[5/2] overflow-hidden rounded-lg">
              <img
                src={curaImg}
                alt="A Música Portuguesa a Gostar Dela Própria"
                className="w-full h-full object-cover grayscale"
                style={{ objectPosition: "50% 80%" }}
              />
            </div>
            <div className="flex flex-col gap-3 pr-8">
              <p>
                A Música Portuguesa a Gostar Dela Própria é um projeto de
                arquivo vivo e celebração da identidade sonora de Portugal.
                Desde 2011, percorre o país de norte a sul, ilhas incluídas,
                registando — em vídeo, som e palavra — músicos, cantores,
                poetas, tocadores e comunidades que mantêm viva a alma da música
                portuguesa.
              </p>
              <p>
                Mais do que um arquivo, é um retrato coletivo. Sem estúdios, sem
                filtros e sem artifícios, cada gravação acontece no lugar de
                origem — na aldeia, na rua, na cozinha, na serra ou à beira-mar
                —, deixando que o som e o silêncio do espaço façam parte da
                canção.
              </p>
              <p>
                O projeto nasceu da vontade de Tiago Pereira de mostrar a força
                da tradição e a sua constante reinvenção. O resultado é um
                mosaico de vozes e expressões que atravessa géneros e gerações —
                do fado à música popular, do canto alentejano à eletrónica, da
                tradição oral à experimentação.
              </p>
              <p>
                A Música Portuguesa a Gostar Dela Própria é, acima de tudo, um
                gesto de escuta. Um país a ouvir-se a si próprio.
              </p>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-3 md:gap-0 mt-8">
                <a
                  className="cursor-pointer text-color-2 hover:text-color-1 transition-all duration-250 underline"
                  href="https://vimeo.com/470587297"
                  target="_blank"
                >
                  O que é a MPAGDP?
                </a>
                <a
                  className="cursor-pointer text-color-2 hover:text-color-1 transition-all duration-250 underline"
                  href="https://vimeo.com/509468023"
                  target="_blank"
                >
                  Qual o papel da MPAGDP?
                </a>
                <a
                  className="cursor-pointer text-color-2 hover:text-color-1 transition-all duration-250 underline"
                  href="mailto:amusicaportuguesa@gmail.com"
                  target="_blank"
                >
                  amusicaportuguesa@gmail.com
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default About;
