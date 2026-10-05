const contactForm = document.getElementById('contact-form');

contactForm.addEventListener('submit', (event) => {
  event.preventDefault();
  if (!contactForm.reportValidity()) return;
  const fields = new FormData(contactForm);
  const name = fields.get('name').trim();
  const email = fields.get('email').trim();
  const organization = fields.get('organization').trim();
  const message = fields.get('message').trim();
  const interest = fields.get('interest').trim();
  const body = [message, '', `Name: ${name}`, `Email: ${email}`,
    organization ? `Lab / organization: ${organization}` : '',
    interest ? `Interest: ${interest}` : ''].filter((line, index) => line || index === 1).join('\n');
  const subject = `Ursa Labs inquiry from ${name}`;
  const draft = `mailto:alex@ursalabs.ai?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
  window.location.href = draft;
  const status = document.getElementById('contact-status');
  status.hidden = false;
  status.textContent = 'If your email app did not open, email alex@ursalabs.ai directly. Your message is still here to copy.';
});
