document.addEventListener('DOMContentLoaded', function() {

    const allEditButtons = document.querySelectorAll('.post__edit-button');
    for (let i = 0; i < allEditButtons.length; i++) {
        allEditButtons[i].addEventListener('click', (e) => editPost(e.target.dataset.postid))
    }

    function editPost(postID) {
    
        // Find relevant elements
        const content = document.querySelector(`#post__content-${postID}`);
        const editButton = document.querySelector(`#post__edit-button-${postID}`);
        const editGroup = document.querySelector(`#post__edit-${postID}`);
        
        // Create and prefill editable textarea
        const editableContent = document.createElement('textarea');
        editableContent.innerHTML = content.innerHTML
        editableContent.style.height = '15ch';
    
        // Clear post content and add editable content
        content.innerHTML = '';
        content.append(editableContent);
    
        // Hide edit button
        editButton.style.display = 'none';
    
        // Create save button
        const saveButton = document.createElement('button');
        saveButton.innerHTML = 'Save';
        saveButton.onclick = async () => {
            const newContent = editableContent.value;
            const csrftoken = getCookie('csrftoken');
            await fetch(`/posts/${postID}`, {
                method: 'POST',
                headers: { 'X-CSRFToken': csrftoken },
                body: JSON.stringify({ newContent: newContent }),
            })
            .then(() => {

                // Update post with new content
                content.innerHTML = newContent;
    
                // Remove save button 
                saveButton.remove();
    
                // Show edit button 
                editButton.style.display = 'block';
            })   
        }
        editGroup.append(saveButton);
    }

    function getCookie(name) {

        let cookieValue = null;
    
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
    
        return cookieValue;
    }

})
