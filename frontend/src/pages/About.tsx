import { useContentReady } from "../composables/usePageTransition";

const About = () => {
  useContentReady(true);

  return <div className="grid-setup">
    <div className="grid grid-cols-1 md:grid-cols-[1fr_2fr] gap-0 md:gap-6 lg:gap-8">
      <div>
        <span className="block h-px w-full bg-color-1 opacity-50 mt-2" />
        <h2>Contactos</h2>
        <div className="flex flex-col">
          <a href="" target="_blank">amusicaportuguesa@gmail.com</a>
          <a href="" target="_blank">Facebook</a>
          <a href="" target="_blank">Instagram</a>
        </div>
      </div>
      <div>
        <span className="block h-px w-full bg-color-1 opacity-50 mt-2" />
        <h2 className="text-title-2 mt-1 mb-3">Sobre o Lastro</h2>
        <p>A Música Portuguesa a Gostar Dela Própria é um projeto de arquivo vivo e celebração da identidade sonora de Portugal. Desde 2011, percorre o país de norte a sul, ilhas incluídas, registando — em vídeo, som e palavra — músicos, cantores, poetas, tocadores e comunidades que mantêm viva a alma da música portuguesa.</p>
        <p>Mais do que um arquivo, é um retrato coletivo. Sem estúdios, sem filtros e sem artifícios, cada gravação acontece no lugar de origem — na aldeia, na rua, na cozinha, na serra ou à beira-mar —, deixando que o som e o silêncio do espaço façam parte da canção.</p>
        <p>O projeto nasceu da vontade de Tiago Pereira de mostrar a força da tradição e a sua constante reinvenção. O resultado é um mosaico de vozes e expressões que atravessa géneros e gerações — do fado à música popular, do canto alentejano à eletrónica, da tradição oral à experimentação.</p>
        <p>A Música Portuguesa a  Gostar Dela Própria é, acima de tudo, um gesto de escuta. Um país a ouvir-se a si próprio.</p>
      </div>
    </div>
  </div>;
};

export default About;
