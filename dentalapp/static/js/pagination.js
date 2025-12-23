


function renderPaginationUI(href, maxPages, totalPages) {
    let pagination = document.getElementById("pagination");
    pagination.innerHTML = "";

    pagination.innerHTML += `
      <li class="page-item ${currentPage === 1 ? 'disabled' : ''}">
        <a class="page-link pre-next" href="#" data-page="prev"><<</a>
      </li>
    `;

    let start = Math.max(1, currentPage - Math.floor(maxPages / 2));
    let end = Math.min(totalPages, start + maxPages - 1);
    start = Math.max(1, end - maxPages + 1);

    for (let i = start; i <= end; i++) {
        pagination.innerHTML += `
          <li class="page-item ${i === currentPage ? 'active' : ''}">
            <a class="page-link" href="${href}?page=${i}" data-page="${i}">${i}</a>
          </li>
        `;
    }

    console.log(pagination);

    pagination.innerHTML += `
      <li class="page-item ${currentPage === totalPages ? 'disabled' : ''}">
        <a class="page-link" href="#" data-page="next">>></a>
      </li>
    `;
}
