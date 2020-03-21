import ClassicEditor from '@ckeditor/ckeditor5-build-classic'

window.addEventListener('DOMContentLoaded', () => {
  Array.from(document.querySelectorAll('.ckeditor')).forEach(elem => {
    ClassicEditor.create(elem)
      .then(editor => {
        console.log(editor)
      })
      .catch(error => {
        console.error(error)
      })
  })
})
