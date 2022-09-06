{
	"///threeslashes",
	&url.URL{
		Path: "///threeslashes",
	},
	"",
},
{
	"http://user:password@testsarp.com",
	&url.URL{
		Scheme: "http",
		User:   url.UserPassword("user", "password"),
		Host:   "testsarp.com",
	},
	"http://user:password@testsarp.com",
},
// unescaped @ in username should not confuse host
{
	"http://j@ne:password@testsarp.com",
	&url.URL{
		Scheme: "http",
		User:   url.UserPassword("j@ne", "password"),
		Host:   "testsarp.com",
	},
	"http://j%40ne:password@testsarp.com",
},
// unescaped @ in password should not confuse host
{
	"http://jane:p@ssword@testsarp.com",
	&url.URL{
		Scheme: "http",
		User:   url.UserPassword("jane", "p@ssword"),
		Host:   "testsarp.com",
	},
	"http://jane:p%40ssword@testsarp.com",
},
{
	"http://j@ne:password@testsarp.com/p@th?q=@go",
	&url.URL{
		Scheme:   "http",
		User:     url.UserPassword("j@ne", "password"),
		Host:     "testsarp.com",
		Path:     "/p@th",
		RawQuery: "q=@go",
	},
	"http://j%40ne:password@testsarp.com/p@th?q=@go",
},
{
	"http://www.testsarp.com/?q=go+language#foo",
	&url.URL{
		Scheme:   "http",
		Host:     "www.testsarp.com",
		Path:     "/",
		RawQuery: "q=go+language",
		Fragment: "foo",
	},
	"",
},
{
	"http://www.testsarp.com/?q=go+language#foo%26bar",
	&url.URL{
		Scheme:   "http",
		Host:     "www.testsarp.com",
		Path:     "/",
		RawQuery: "q=go+language",
		Fragment: "foo&bar",
	},
	"http://www.testsarp.com/?q=go+language#foo&bar",
},