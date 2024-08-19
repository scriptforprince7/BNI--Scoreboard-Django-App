document.querySelectorAll('.list-group-item').forEach(item => {
  item.addEventListener('click', function() {
      const scoreType = this.textContent.split(' ')[0];
      const tips = {
          'Absent': 'To improve your attendance, consider setting daily alarms and prioritizing your schedule.',
          'Late': 'Avoid tardiness by planning your commute and leaving earlier.',
          'Referral': 'Increase referrals by networking more and discussing the benefits of our services.',
          'Visitors': 'Engage with more visitors by being more active in customer-facing roles.',
          'TYFCB': 'Encourage customer loyalty by thanking them for their business regularly.',
          'Training': 'Enhance your skills by attending more training sessions.',
          'Testimonial': 'Collect more testimonials by asking satisfied customers to share their experiences.',
          'Projected': 'Focus on your overall performance to improve your projected scores.'
      };
      document.getElementById('tipContent').textContent = tips[scoreType] || 'No tips available.';
  });
});
