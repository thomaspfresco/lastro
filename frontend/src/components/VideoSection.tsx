interface VideoSectionProps {
  project: Project;
}

function formatDate(dateString: string): string {
  const date = new Date(dateString);
  const day = String(date.getDate()).padStart(2, '0');
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const year = date.getFullYear();
  return `${day}-${month}-${year}`;
}

export default function VideoSection({ project }: VideoSectionProps) {
  return (
    <div className="mb-12 grid grid-cols-1 lg:grid-cols-2 gap-4 items-start">
      <div className="aspect-video w-full">
        <iframe
          key={project.id}
          src={`https://player.vimeo.com/video/${project.id}?chromecast=0`}
          className="w-full h-full border-0"
          allow="autoplay; fullscreen; picture-in-picture"
          title={project.title}
        ></iframe>
      </div>

      <div className="flex flex-col justify-center gap-8">
        <div className="grid grid-cols-2 gap-8">
          <div className="flex flex-col gap-4">
            {project.category && project.category !== "" && (
              <div>
                <p className="text-note-3 uppercase opacity-50 mb-0.5">
                  Categoria
                </p>
                <p className="text-body-1 break-words">{project.category}</p>
              </div>
            )}

            {project.date && project.date !== "" && (
              <div>
                <p className="text-note-3 uppercase opacity-50 mb-0.5">Data</p>
                <p className="text-body-1">{formatDate(project.date)}</p>
              </div>
            )}
          </div>
          {project.location && project.location !== "" ? (
            <div>
              <p className="text-note-3 uppercase opacity-50 mb-0.5">
                Localização
              </p>
              <p className="text-body-1">{project.location}</p>
            </div>
          ) : (
            <div />
          )}
        </div>

        <div className="flex flex-col">
          {project.keywords && project.keywords !== "" && (
            <div>
              <p className="text-note-3 uppercase opacity-50 mb-1">
                Palavras-chave
              </p>
              <p className="text-body-1">{project.keywords}</p>
            </div>
          )}
        </div>

        <div className="grid grid-cols-2 md:grid-cols-3 gap-x-8 gap-y-4">
          {project.direction && project.direction !== "" && (
            <div>
              <p className="text-note-3 uppercase opacity-50 mb-0.5">Direção</p>
              <p className="text-body-1">{project.direction}</p>
            </div>
          )}

          {project.sound && project.sound !== "" && (
            <div>
              <p className="text-note-3 uppercase opacity-50 mb-0.5">Som</p>
              <p className="text-body-1">{project.sound}</p>
            </div>
          )}

          {project.production && project.production !== "" && (
            <div>
              <p className="text-note-3 uppercase opacity-50 mb-0.5">
                Produção
              </p>
              <p className="text-body-1">{project.production}</p>
            </div>
          )}

          {project.support && project.support !== "" && (
            <div>
              <p className="text-note-3 uppercase opacity-50 mb-0.5">Apoio</p>
              <p className="text-body-1">{project.support}</p>
            </div>
          )}

          {project.assistance && project.assistance !== "" && (
            <div>
              <p className="text-note-3 uppercase opacity-50 mb-0.5">
                Assistência
              </p>
              <p className="text-body-1">{project.assistance}</p>
            </div>
          )}

          {project.research && project.research !== "" && (
            <div>
              <p className="text-note-3 uppercase opacity-50 mb-0.5">
                Pesquisa
              </p>
              <p className="text-body-1">{project.research}</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
