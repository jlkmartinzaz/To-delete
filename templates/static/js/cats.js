async function getCats(token) {
  return apiRequest("/", "GET", null, token);
}

async function createCat(token, name, breed, age) {
  return apiRequest("/", "POST", { name, breed, age }, token);
}
