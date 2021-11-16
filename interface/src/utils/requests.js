export const getRequest = (url) => {
  const headers = {
    "Content-Type": "application/json",
  };

  const urlInstance = new URL(url);

  return fetch(urlInstance.toString(), { headers }).then((result) => {
    return result.json();
  });
};

export const postRequest = (url, body) => {
  const headers = {
    "Content-Type": "application/json",
  };

  const init = {
    method: "POST",
    headers,
    body: JSON.stringify(body),
  };

  return fetch(url, init).then((result) => {
    return result.json();
  });
};
