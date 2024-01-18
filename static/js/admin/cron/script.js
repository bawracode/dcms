document.addEventListener("DOMContentLoaded", function () {
  // getCookie function: fetch cookie from browser
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  // csrf token for ajax request
  const csrftoken = getCookie("csrftoken");

  let checkbox = document.querySelectorAll(
    ".django-toggle-switch input[type=checkbox]"
  );
  checkbox.forEach(function (checkbox) {
    checkbox.addEventListener("change", statusCheckboxChanged);
  });

  async function change_toggle(id, status) {
    const url = `/cron/toggle/`;

    try {
      const response = await fetch(url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-Requested-With": "XMLHttpRequest",
          "X-CSRFToken": csrftoken,
        },
        body: JSON.stringify({
          id: id,
          status: status,
        }),
      });

      if (!response.ok) {
        throw new Error("Error: " + response.status);
      }
      const responseData = await response.json();

      return responseData["status"];
    } catch (error) {
      console.error("Error:", error);
    }
  }

  async function statusCheckboxChanged(e) {
    button_status = e.target.checked;
    button_id = e.target.id;

    let result = await change_toggle(button_id, button_status);
    console.log(result);
  }
});
