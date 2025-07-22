import { useEffect, useState } from "react";

const definitions = [
  "[Marinha] Areia, barras de metal ou outro peso que se mete no fundo do porão do navio que não leva bastante ou nenhuma carga.",
  "Sacos de areia que vão na barquinha do aeróstato.",
  "[Figurado] O que se come para dar azo a beber.",
  "Base (em que se firma alguma coisa).",
  "Tudo o que faz aguentar o peso.",
];

const Definitions = () => {
  const [current, setCurrent] = useState(0);
  const [fade, setFade] = useState(true);

  useEffect(() => {
    const interval = setInterval(() => {
      setFade(false); // inicia fade out
      setTimeout(() => {
        setCurrent((prev) => (prev + 1) % definitions.length);
        setFade(true); // inicia fade in
      }, 700); // duração do fade out
    }, 5000); // tempo total por slide

    return () => clearInterval(interval);
  }, []);

  const handleClick = () => {
    window.open("https://dicionario.priberam.org/lastro", "_blank", "noopener,noreferrer");
  };

  return (
    <div
      onClick={handleClick}
      className="text-xs font-dm_light text-white/50 hover:text-[#FA7D00] hover:cursor-pointer select-none"
      role="button"
      tabIndex={0}
      onKeyDown={(e) => {
        if (e.key === "Enter" || e.key === " ") {
          e.preventDefault();
          handleClick();
        }
      }}
      aria-label="Abrir definição no Priberam"
    >
      <p>(las·tro) · nome masculino</p>
      <p
        className={`mt-0.5 transition-opacity duration-700 ${
          fade ? "opacity-100" : "opacity-0"
        }`}
        aria-live="polite"
      >
        {definitions[current]}
      </p>
    </div>
  );
};

export default Definitions;
