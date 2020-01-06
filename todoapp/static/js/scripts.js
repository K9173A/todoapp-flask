function toggleTasksVisibility() {
  const hasTasks = $('.task').length > 0;
  $('.tasks').toggle(hasTasks);
  $('.empty').toggle(!hasTasks);
}

$(function () {
  let removeItemURL = null;

  // Creates task
  $('#save-btn').on('click', function () {
    const modal = $('#modal-create-task');
    const form = modal.find('form');
    $.post(
      form.attr('action'),
      form.serialize(),
      data => {
        if (data.form_is_valid) {
          $('.tasks').html(data.tasks_html);
          modal.modal('toggle');
          toggleTasksVisibility();
        } else {
          form.html(data.form_html);
        }
      }
    );
  });

  // Deletes task
  $('#delete-btn').on('click', function () {
    const modal = $('#modal-confirm-delete');
    $.ajax({
      url: removeItemURL,
      type: 'DELETE',
      success: data => {
        console.log(data);
        $('.tasks').html(data.tasks_html);
        modal.modal('toggle');
        toggleTasksVisibility();
      }
    });
  });

  // Shows up modal window (bootstrap js) and registers url of item.
  $('.tasks').on('click', '.delete-btn', function (event) {
    removeItemURL = event.target.dataset.url;
  });

  // Shows up modal window for item creation.
  $('.create-btn').on('show.bs.modal', function () {
    const form = $(this).find('form');
    $.get(
      form.attr('action'),
      data => form.html(data.form_html)
    );
  });
});

toggleTasksVisibility();
