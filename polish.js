document.addEventListener('DOMContentLoaded', () => {
  const memberIds = [
    'mypage',
    'points',
    'coupon',
    'history',
    'settings',
    'profile',
    'notice',
    'contract',
    'upgrade',
    'payment',
    'other',
    'other2',
    'receipt',
    'namechange',
    'pause',
    'pausetrap',
    'faq1',
    'faqanswer',
    'retain1',
    'other3',
    'applydoor',
    'boss1',
    'resetloop',
    'boss2',
    'closeTrap',
    'boss3',
    'boss4',
    'boss5',
    'reasontrap',
    'boss6',
    'runnerCaught',
    'boss7',
    'wrongLearned',
    'boss8',
    'chat1',
    'chat2',
    'chat3',
    'callback',
    'boss9',
    'surveytrap',
    'boss10',
    'stayfinal',
    'fakeend',
    'mail',
    'lastlogin',
  ];

  document.querySelectorAll('.immersive a,.immersive button,.immersive input').forEach((el) => {
    el.addEventListener('focus', () => document.body.classList.add('keyboard-focus'), {
      once: true,
    });
  });

  const updateContext = () => {
    const id = location.hash.replace('#', '') || 'start';
    document.body.classList.toggle('in-member-service', memberIds.includes(id));
  };
  updateContext();
  window.addEventListener('hashchange', updateContext);
});
