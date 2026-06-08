// OmniSenter Blog — auto-add a "Share to X" button to every blog post
// and any page that opts in via class="share-x-target"

document.addEventListener('DOMContentLoaded', function() {
  // Find all H1 elements in blog posts
  const articles = document.querySelectorAll('.md-content .md-typeset');
  if (!articles.length) return;

  // Get the page title
  const titleEl = document.querySelector('h1');
  if (!titleEl) return;
  const title = titleEl.textContent.trim();

  // Get the page URL
  const url = encodeURIComponent(window.location.href);
  const text = encodeURIComponent(title + ' — OmniSenter blog');

  // Build the share link
  const shareLink = `https://x.com/intent/post?text=${text}&url=${url}`;

  // Find the first paragraph after the hero (skip hero images)
  const firstP = titleEl.closest('.md-content').querySelector('.md-typeset > p, .md-typeset > blockquote');

  if (firstP) {
    // Insert the share button right after the first paragraph
    const btn = document.createElement('a');
    btn.href = shareLink;
    btn.target = '_blank';
    btn.rel = 'noopener';
    btn.className = 'share-x';
    btn.textContent = 'Share on X';
    firstP.parentNode.insertBefore(btn, firstP.nextSibling);
  }
});
