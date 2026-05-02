function SearchPicture(event) {
  event.preventDefault();

  const search = document.getElementById("search-input").value;
  const img = document.getElementById("pic");
  const desc = document.getElementById("desc");

  fetch("/search?s=" + search, {
    method: "GET",
  })
    .then((response) => response.json())

    .then((data) => {
      img.src = "/picture?p=" + data.data.picture;
      desc.innerHTML = data.data.description;
      search.value = "";
    })

    .catch((error) => {
      console.error("request failed: ", error);
    });
}
