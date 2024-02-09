document.addEventListener('DOMContentLoaded', function() {

    likeButton()
    unlikeButton()

    // Edit button
    document.querySelectorAll('.post__edit-button').forEach( (editButton) => {
        editButton.addEventListener('click', (e) => editPost(e.target.dataset.postid))
    })

    function likeButton() {
        document.querySelectorAll('.post__like-button').forEach( likeButton => {
            const postID = likeButton.dataset.postid;
            isPostLiked(postID)
            .then( response => {
                likeButton.style.display = !response.isLiked ? 'flex' : 'none';
                likeButton.onclick = () => {
                    likePost(postID).then(() => {
                        getLikes(postID).then(response => document.querySelector(`#post__likes-${postID}`).innerHTML = response.likes);
                        likeButton.style.display = 'none';
                        document.querySelector(`#post__unlike-button-${postID}`).style.display = 'flex';
                    })
                }
            })
        })
    }

    function unlikeButton() {
        document.querySelectorAll('.post__unlike-button').forEach( unlikeButton => {
            const postID = unlikeButton.dataset.postid;
            isPostLiked(postID)
            .then(response => {
                unlikeButton.style.display = response.isLiked ? 'flex' : 'none';
                unlikeButton.onclick = () => {
                    unlikePost(postID).then(() => {
                        getLikes(postID).then(response => document.querySelector(`#post__likes-${postID}`).innerHTML = response.likes);
                        unlikeButton.style.display = 'none';
                        document.querySelector(`#post__like-button-${postID}`).style.display = 'flex';
                    })
                }
            })
        })
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
            await fetch(`/posts/edit/${postID}`, {
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
    
    async function isPostLiked(postID) {

        const response = await fetch(`/posts/is_liked/${postID}`, {
            method: 'GET',
            cache: 'no-store',
        });

        return await response.json();
    }

    async function likePost(postID) {
        
        const csrftoken = getCookie('csrftoken');

        const response = await fetch(`/posts/like/${postID}`, {
            method: 'POST',
            headers: { 'X-CSRFToken': csrftoken },
        });

        return await response.json();
    
    }
    async function unlikePost(postID) {
        
        const csrftoken = getCookie('csrftoken');

        const response = await fetch(`/posts/unlike/${postID}`, {
            method: 'POST',
            headers: { 'X-CSRFToken': csrftoken },
        });

        return await response.json();
    }

    async function getLikes(postID) {

        const response = await fetch(`/posts/get_likes/${postID}`)

        return await response.json()
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
