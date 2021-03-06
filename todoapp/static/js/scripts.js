function toggleTasksVisibility() {
  const hasTasks = $('.task').length > 0;
  $('.tasks').toggle(hasTasks);
  $('.empty').toggle(!hasTasks);
}

$(function () {
  let taskId = null;
  const tasks = $('.tasks');
  const pagination = $('.pagination-wrapper');

  // Creates task
  $('#save-btn').on('click', function () {
    const modal = $('#modal-create-task');
    const form = modal.find('form');
    $.post(
      form.attr('action'),
      form.serialize(),
      data => {
        if (data.form_is_valid) {
          pagination.html(data.pagination_html);
          tasks.html(data.tasks_html);
          modal.modal('toggle');
          toggleTasksVisibility();
        } else {
          form.html(data.form_html);
        }
      }
    );
  });

  // Updates task
  $('#update-btn').on('click', function () {
    const modal = $('#modal-update-task');
    const form = modal.find('form');
    $.ajax({
      url: `${form.attr('action')}?task=${taskId}`,
      type: 'PUT',
      data: form.serialize(),
      success: data => {
        if (data.form_is_valid) {
          pagination.html(data.pagination_html);
          tasks.html(data.tasks_html);
          modal.modal('toggle');
          toggleTasksVisibility();
        } else {
          form.html(data.form_html);
        }
      }
    });
  });

  // Deletes task
  $('#delete-btn').on('click', function () {
    const modal = $('#modal-confirm-delete');
    $.ajax({
      url: `${this.dataset.url}?task=${taskId}`,
      type: 'DELETE',
      success: data => {
        pagination.html(data.pagination_html);
        tasks.html(data.tasks_html);
        modal.modal('toggle');
        toggleTasksVisibility();
      }
    });
  });

  // Shows up modal window (bootstrap js) and registers url of item.
  tasks.on('click', '.save-task-id', function () {
    taskId = this.dataset.task;
  });

  // Shows up modal window
  $(document).on('show.bs.modal', '#modal-create-task', function () {
    const form = $(this).find('form');
    $.get(form.attr('action'), data => form.html(data.form_html));
  });
  $(document).on('show.bs.modal', '#modal-update-task',function () {
    const form = $(this).find('form');
    $.get(`${form.attr('action')}?task=${taskId}`, data => form.html(data.form_html));
  });

  // Applies filters
  $('#filter-btn').on('click', function () {
    const form = $('#filter-form');
    const sortFilterValue = form.find('.filter-sort input:radio').val();
    $.ajax({
      url: `${form.attr('action')}?sort=${sortFilterValue}`
    })
  })
});

toggleTasksVisibility();
