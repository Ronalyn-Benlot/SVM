const btnElList = document.querySelectorAll('.btn');

btnElList.forEach(btnEl =>{
	btnEl.addEventListener('click', () => {
		document.querySelector('.special')?.classList.remove('special');
		btnEl.classList.add('special');
	});
});