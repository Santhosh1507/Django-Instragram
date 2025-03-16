function toggleCommentSection() {
  const commentSection = document.querySelector(".comment-section");
  if (
    commentSection.style.display === "none" ||
    commentSection.style.display === ""
  ) {
    commentSection.style.display = "block";
  } else {
    commentSection.style.display = "none";
  }
}

function closeModal() {
  document.getElementById("exampleModal").classList.add("hidden");
}

function openModal() {
  document.getElementById("exampleModal").classList.remove("hidden");
}
function closeSearchModal() {
  document.getElementById("exampleModal3").classList.add("hidden");
}


console.log("Modal");




document.addEventListener("DOMContentLoaded", function () {
  function openCreatePostModal() {
    const modal = document.getElementById("exampleModal2");
    if (modal) {
      modal.classList.remove("hidden");
    } else {
      console.error("Modal with id 'exampleModal2' not found!");
    }
  }

  function closeCreatePostModal() {
    const modal = document.getElementById("exampleModal2");
    if (modal) {
      modal.classList.add("hidden");
    } else {
      console.error("Modal with id 'exampleModal2' not found!");
    }
  }

  // Attach event listeners to buttons (if needed)
  const openModalButton = document.getElementById("openCreatePostModalButton");
  if (openModalButton) {
    openModalButton.addEventListener("click", openCreatePostModal);
  }

  const closeModalButton = document.getElementById("closeCreatePostModalButton");
  if (closeModalButton) {
    closeModalButton.addEventListener("click", closeCreatePostModal);
  }
});



document.addEventListener("DOMContentLoaded", function () {
  function openCreatePostModal() {
    const modal = document.getElementById("exampleModal1");
    if (modal) {
      modal.classList.remove("hidden");
    } else {
      console.error("Modal with id 'exampleModal1' not found!");
    }
  }

  function closeCreatePostModal() {
    const modal = document.getElementById("exampleModal1");
    if (modal) {
      modal.classList.add("hidden");
    } else {
      console.error("Modal with id 'exampleModal1' not found!");
    }
  }

  // Attach event listeners to buttons (if needed)
  const openModalButton = document.getElementById("openEditProfileModalbutton");
  if (openModalButton) {
    openModalButton.addEventListener("click", openCreatePostModal);
  }

  const closeModalButton = document.getElementById("EditProfileModalbutton");
  if (closeModalButton) {
    closeModalButton.addEventListener("click", closeCreatePostModal);
  }
});



function toggleCommentSection(postId) {
  const commentSection = document.getElementById(`openCommentSection-${postId}`);
  const toggleButton = document.getElementById(`toggleCommentBtn-${postId}`);

  // Toggle visibility
  if (commentSection.classList.contains('hidden')) {
    commentSection.classList.remove('hidden');
    toggleButton.innerHTML = '<i class="fa-solid fa-comment mr-2"></i> Hide Comments'; // Change button text
  } else {
    commentSection.classList.add('hidden');
    toggleButton.innerHTML = '<i class="fa-solid fa-comment mr-2"></i> Comment'; // Reset button text
  }
}




  function checkNotifications() {
      fetch('/check-notifications')
          .then(response => response.json())
          .then(data => {
              const dot = document.getElementById('notification-dot');
              if (data.unread_count > 0) {
                  dot.classList.remove('hidden'); // Show red dot
                  playNotificationSound();
              } else {
                  dot.classList.add('hidden'); // Hide red dot
              }
          });
  }

  function playNotificationSound() {
      const audio = new Audio("{% static 'sounds/notification.mp3' %}");
      audio.play();
  }

  function clearNotificationDot() {
      document.getElementById('notification-dot').classList.add('hidden');
  }

  // Check notifications every 10 seconds
  setInterval(checkNotifications, 10000);
  checkNotifications();

