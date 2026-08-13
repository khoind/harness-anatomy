function installTopTableOfContents() {
  const article = document.querySelector("article.md-content__inner");
  const heading = article?.querySelector("h1");
  const sourceList = document.querySelector(
    ".md-sidebar--primary .md-nav--primary > .md-nav__list"
  );

  if (!article || !heading || !sourceList || article.querySelector(".top-toc")) {
    return;
  }

  const details = document.createElement("details");
  details.className = "top-toc";

  const summary = document.createElement("summary");
  summary.textContent = "Contents";

  const contents = document.createElement("nav");
  contents.className = "top-toc__contents";
  contents.setAttribute("aria-label", "Site contents");
  contents.append(sourceList.cloneNode(true));

  details.append(summary, contents);
  heading.insertAdjacentElement("afterend", details);
}

document.addEventListener("DOMContentLoaded", installTopTableOfContents);