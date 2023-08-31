document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // Submit handler
  document.querySelector('#compose-form').addEventListener('submit', send_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

async function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#mailbox-view').style.display = 'block';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#mailbox-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // GET request to /emails/<mailbox>
  await fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {

      // Load emails
      emails.forEach(email => {

        // Create new email
        document.querySelector('#mailbox-view').className = 'list-group'
        document.querySelector('#mailbox-view').classList.add('list-group-flush')
        const content = document.createElement('div')
        content.className = `mailbox-item-${email.id} list-group-item`
        email.read ? content.classList.add('read') : content.classList.remove('read')
        content.innerHTML = `
          <div class="mailbox-item__info">
            <span>${email.sender}</span>
            <span class="mailbox-item__subject">${email.subject}</span>
            <span class="mailbox-item__timestamp">${email.timestamp}</span>
          </div>
          <div class="mailbox-item__body">${email.body}</div>
        `;

        // Create email buttons for relevant mailboxes
        if (mailbox != 'sent') {
          
          // Button group 
          const buttonGroup = document.createElement('div')
          buttonGroup.className = 'mailbox-item__button-group hidden'
          buttonGroup.onclick = async (e) => { e.stopPropagation() }

          // Archive button
          const archiveButton = document.createElement('button')
          archiveButton.className = 'mailbox-item__archive-button btn btn-outline-secondary btn-sm'
          const archiveSVG = '<svg xmlns="http://www.w3.org/2000/svg" height="1em" viewBox="0 0 512 512"><!--! Font Awesome Free 6.4.2 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2023 Fonticons, Inc. --><path d="M32 32H480c17.7 0 32 14.3 32 32V96c0 17.7-14.3 32-32 32H32C14.3 128 0 113.7 0 96V64C0 46.3 14.3 32 32 32zm0 128H480V416c0 35.3-28.7 64-64 64H96c-35.3 0-64-28.7-64-64V160zm128 80c0 8.8 7.2 16 16 16H336c8.8 0 16-7.2 16-16s-7.2-16-16-16H176c-8.8 0-16 7.2-16 16z"/></svg>'
          const unarchiveSVG = '<svg xmlns="http://www.w3.org/2000/svg" height="1em" viewBox="0 0 512 512"><!--! Font Awesome Free 6.4.2 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2023 Fonticons, Inc. --><path d="M121 32C91.6 32 66 52 58.9 80.5L1.9 308.4C.6 313.5 0 318.7 0 323.9V416c0 35.3 28.7 64 64 64H448c35.3 0 64-28.7 64-64V323.9c0-5.2-.6-10.4-1.9-15.5l-57-227.9C446 52 420.4 32 391 32H121zm0 64H391l48 192H387.8c-12.1 0-23.2 6.8-28.6 17.7l-14.3 28.6c-5.4 10.8-16.5 17.7-28.6 17.7H195.8c-12.1 0-23.2-6.8-28.6-17.7l-14.3-28.6c-5.4-10.8-16.5-17.7-28.6-17.7H73L121 96z"/></svg>'
          archiveButton.innerHTML = email.archived ? `${unarchiveSVG}Unarchive` : `${archiveSVG}Archive`
          archiveButton.addEventListener('click', async () => {
            await fetch(`/emails/${email.id}`, {
              method: 'PUT',
              body: JSON.stringify({
                  archived: !email.archived
              })
            })
            .then(() => { load_mailbox('inbox') })
          })

          // Read button
          const readButton = document.createElement('button')
          readButton.className = 'mailbox-item__read-button btn btn-outline-secondary btn-sm'
          const readSVG = '<svg xmlns="http://www.w3.org/2000/svg" height="1em" viewBox="0 0 512 512"><!--! Font Awesome Free 6.4.2 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2023 Fonticons, Inc. --><path d="M64 208.1L256 65.9 448 208.1v47.4L289.5 373c-9.7 7.2-21.4 11-33.5 11s-23.8-3.9-33.5-11L64 255.5V208.1zM256 0c-12.1 0-23.8 3.9-33.5 11L25.9 156.7C9.6 168.8 0 187.8 0 208.1V448c0 35.3 28.7 64 64 64H448c35.3 0 64-28.7 64-64V208.1c0-20.3-9.6-39.4-25.9-51.4L289.5 11C279.8 3.9 268.1 0 256 0z"/></svg>'
          const unreadSVG = '<svg xmlns="http://www.w3.org/2000/svg" height="1em" viewBox="0 0 512 512"><!--! Font Awesome Free 6.4.2 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2023 Fonticons, Inc. --><path d="M48 64C21.5 64 0 85.5 0 112c0 15.1 7.1 29.3 19.2 38.4L236.8 313.6c11.4 8.5 27 8.5 38.4 0L492.8 150.4c12.1-9.1 19.2-23.3 19.2-38.4c0-26.5-21.5-48-48-48H48zM0 176V384c0 35.3 28.7 64 64 64H448c35.3 0 64-28.7 64-64V176L294.4 339.2c-22.8 17.1-54 17.1-76.8 0L0 176z"/></svg>'
          readButton.innerHTML = email.read ? `Mark as${unreadSVG}` : `Mark as${readSVG}`
          readButton.addEventListener('click', async () => {
            await fetch(`/emails/${email.id}`, {
              method: 'PUT',
              body: JSON.stringify({
                  read: !email.read
              })
            })
            .then(() => { load_mailbox(mailbox) })
          })

          // Append buttons to button group and button group to email
          buttonGroup.append(archiveButton, readButton)
          content.append(buttonGroup)
          
          // Show button group when hovering an email
          content.onmouseenter = function() { buttonGroup.classList.remove('hidden') }
          content.onmouseleave = function() { buttonGroup.classList.add('hidden') }
        }

        // Load email
        content.addEventListener('click', function() { load_email(email.id) })

        // Add email to DOM
        document.querySelector('#mailbox-view').append(content)
      });
  });
}

async function load_email(email_id) {
  // Show email and hide other views
  document.querySelector('#mailbox-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // GET request to /emails/<email_id>
  await fetch(`emails/${email_id}`)
  .then(response => response.json())
  .then(async (email) => {

      // Mark email as read
      await fetch(`/emails/${email_id}`, {
        method: 'PUT',
        body: JSON.stringify({
            read: true
        })
      })

      // Load email
      const content = document.querySelector('.email')
      content.innerHTML = `
        <div class="email__info">
          <h5>${email.subject}</h5>
          <h6>${email.sender}</h6>
          <p>${email.timestamp}</p>
          <p><span>To: </span>${email.recipients.join(', ')}</p>
        </div>
      `;
      const bodySplits = email.body.split('\n')
      const emailBody = document.createElement('div')
      emailBody.className = 'email__body'
      bodySplits.forEach(split => {
        if (split === '' || split === '    ') {
          const linebreak = document.createElement('br')
          emailBody.append(linebreak)
        } else {
          const element = document.createElement('div')
          element.innerHTML = split
          emailBody.append(element)
        }
      })
      content.append(emailBody)
      
      const replyButton = document.querySelector('.email__reply-button')
      replyButton.onclick = async () => { await compose_reply(email_id) }
  });
}

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#mailbox-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Alter heading
  document.querySelector('#compose-view').querySelector('h3').innerHTML = 'New Email'

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

async function compose_reply(email_id) {

  // Show compose view and hide other views
  document.querySelector('#mailbox-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Alter heading
  document.querySelector('#compose-view').querySelector('h3').innerHTML = 'Reply Email'

  // GET request to /emails/<email_id>
  await fetch(`emails/${email_id}`)
  .then(response => response.json())
  .then(async (email) => { 

    // Pre-fill composition fields
    document.querySelector('#compose-recipients').value = email.sender
    document.querySelector('#compose-subject').value = email.subject.startsWith('Re: ') ? email.subject : `Re: ${email.subject}`
    document.querySelector('#compose-body').value = `
    
    >> On ${email.timestamp} ${email.sender} wrote: 
    ${email.body}`;
  })
}

async function send_email(event) {

  event.preventDefault();

  // Get composition fields
  const recipients = document.querySelector('#compose-recipients').value;
  const subject = document.querySelector('#compose-subject').value;
  const body = document.querySelector('#compose-body').value;

  // POST request to /emails
  await fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: recipients,
        subject: subject,
        body: body
    })
  })
  .then(response => response.json())
  .then(result => {

    // Load sent mailbox
      load_mailbox('sent');
  })
}