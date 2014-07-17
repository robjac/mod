autowatch = 1;

inlets = 1;
outlets = 1;

var finder;
var m4lcomp = 0;
var M4LCOMPONENT=new RegExp(/(M4LInterface)/);
var control_names = [];
var controls = {};
var excluded = ['control', 'control_names', 'done'];
debug = Debug;
forceload = Forceload;

if(typeof(String.prototype.trim) === "undefined")
{
	String.prototype.trim = function()
	{
		return String(this).replace(/^\s+|\s+$/g, '');
	};
}

function init()
{
	finder = new LiveAPI(callback, 'control_surfaces', 0);
	var components = finder.get('components');
	for (var i in components)
	{
		finder.id = components[i]
		if(M4LCOMPONENT.test(finder.get('name'))>0)
		{
			m4lcomp = finder.id;
			break;
		}
	}
	if (m4lcomp)
	{
		debug('found m4linterface');
		var names = finder.call('get_control_names');
		for (var i in names)
		{
			var name = names[i];
			if((name!='control_names')&&(name!='control')&&(name!='done'))
			{
				try
				{
					controls[names[i]] = 0;
				}
				catch(err)
				{
				}
			}
		}
	}
}

function get_control_names()
{
	for(var i in controls)
	{
		outlet(0, i);
	}
}

function make_callback(name)
{
	var callback = function(args)
	{
		//debug('callback closure:', args);
		outlet(0, name, args);
	}
	return callback;
}

function grab(name)
{
	if(controls[name]!=undefined)
	{
		if(controls[name]==0)
		{
			var control = finder.call('get_control', name);
			debug('control is:', control);
			controls[name] = new LiveAPI(make_callback(name), control);
			debug('control:', control, controls[name].id);
		}
		finder.call('grab_control', 'id', controls[name].id);
		controls[name].property = 'value';
	}
	else
	{
		debug('Control name:', name, 'isnt registered.');
	}
}

function release(name)
{
	if(controls[name]!=undefined)
	{
		if(controls[name]!=0)
		{
			controls[name].property = '';
			finder.call('release_control', 'id', controls[name].id);
		}
		else
		{
			debug('Control name:', name, 'hasnt been registered yet.  You need to grab it first.');
		}
	}
	else
	{
		debug('Control name:', name, 'isnt registered.');
	}
}

function callback(args){}

forceload(this);