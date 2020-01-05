function toggleTasksVisibility() {
  const hasTasks = $('.task').length > 0;
  $('.tasks').toggle(hasTasks);
  $('.empty').toggle(!hasTasks);
}

$(function () {
  // Creates task
  $('#save-btn').on('click', function () {
    let modal = $('#modal-create-task');
    let form = modal.find('form');
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

  // Shows up modal window
  $('.create-btn').on('show.bs.modal', function () {
    let form = $(this).find('form');
    $.get(
      form.attr('action'),
      data => form.html(data.form_html)
    )
  })

  // Deletes task
  $('')
});

toggleTasksVisibility();
