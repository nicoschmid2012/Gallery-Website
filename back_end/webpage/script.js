function SearchPicture(event) {
  event.preventDefault();

  const search = document.getElementById("search-input").value;
  const img = document.getElementById("pic3");
  const desc = document.getElementById("desc3");

  fetch("/search?s=" + search, {
    method: "GET",
  })
    .then((response) => response.json())

    .then((data) => {
      img.src = "/picture/" + data.data.picture;
      desc.innerHTML = data.data.description;
    })

    .catch((error) => {
      console.error("request failed: ", error);
    });
}
