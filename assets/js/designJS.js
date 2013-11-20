// JavaScript Document

function showLostForm()
{
	document.getElementById("lostFormContainer").style.left ="0em";
}

function hideLostForm()
	{
		document.getElementById("lostFormContainer").style.left ="100%";
	}

function resetLostForm()
{
	document.getElementById("lostForm").reset();
}

function submitLostForm()
{
	document.getElementById("lostForm").submit();
}



function showFoundForm()
{
	document.getElementById("foundFormContainer").style.left ="0em";
}

function hideFoundForm()
	{
		document.getElementById("foundFormContainer").style.left ="100%";
	}

function resetFoundForm()
{
	document.getElementById("foundForm").reset();
}

function submitFoundForm()
{
	document.getElementById("foundForm").submit();
}