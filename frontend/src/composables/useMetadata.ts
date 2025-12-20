import { useEffect } from "react";
import { metadata } from "../config/metadata";

export function useMetadata() {
  useEffect(() => {
    // Update title
    document.title = metadata.title;

    // Update or create meta tags
    const updateMetaTag = (name: string, content: string, isProperty = false) => {
      const attribute = isProperty ? "property" : "name";
      let element = document.querySelector(
        `meta[${attribute}="${name}"]`
      ) as HTMLMetaElement;

      if (!element) {
        element = document.createElement("meta");
        element.setAttribute(attribute, name);
        document.head.appendChild(element);
      }

      element.content = content;
    };

    // SEO meta tags
    updateMetaTag("title", metadata.title);
    updateMetaTag("description", metadata.description);
    updateMetaTag("keywords", metadata.keywords);
    updateMetaTag("author", metadata.author);
    updateMetaTag("theme-color", metadata.themeColor);

    // Open Graph
    updateMetaTag("og:type", "website", true);
    updateMetaTag("og:url", metadata.url, true);
    updateMetaTag("og:title", metadata.title, true);
    updateMetaTag("og:description", metadata.description, true);
    updateMetaTag("og:image", metadata.ogImage, true);

    // Twitter
    updateMetaTag("twitter:card", "summary_large_image", true);
    updateMetaTag("twitter:url", metadata.url, true);
    updateMetaTag("twitter:title", metadata.title, true);
    updateMetaTag("twitter:description", metadata.description, true);
    updateMetaTag("twitter:image", metadata.ogImage, true);

    // Update canonical link
    let canonical = document.querySelector(
      'link[rel="canonical"]'
    ) as HTMLLinkElement;
    if (!canonical) {
      canonical = document.createElement("link");
      canonical.rel = "canonical";
      document.head.appendChild(canonical);
    }
    canonical.href = metadata.url;
  }, []);
}
