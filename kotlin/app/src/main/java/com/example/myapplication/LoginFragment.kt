package com.example.myapplication


import android.content.SharedPreferences
import android.content.Context
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.fragment.app.Fragment
import kotlinx.android.synthetic.main.login_fragment.*
import kotlinx.android.synthetic.main.login_fragment.view.*
import okhttp3.OkHttpClient
import okhttp3.Request
import org.jetbrains.anko.AnkoLogger
import org.jetbrains.anko.doAsync
import org.jetbrains.anko.info
import org.jetbrains.anko.uiThread
import org.jetbrains.anko.activityUiThread
import org.json.JSONArray

/**
 * Fragment representing the login screen for Shrine.
 */
class LoginFragment : Fragment(), AnkoLogger {

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?
    ): View? {
        val view = inflater.inflate(R.layout.login_fragment, container, false)
        //put things into pref file to check against later
        /*var userCheck = activity?.getPreferences(Context.MODE_PRIVATE)
        userCheck?.edit()?.putString("username", "")?.apply()*/
        println("hello")
        view.login_button.setOnClickListener {
            doAsync {
                println("nope")
                //var gotresponse = checkLoginInfo(view.username_text.text.toString(), view.password_text.text.toString())
                val gotresponse = fetchInfo()
                println("will this work?")
                val jsonarray = JSONArray(gotresponse)
                println("hello")

                uiThread {
                    for (i in 0..(jsonarray.length() - 1)) {
                        val user = jsonarray.getJSONObject(i)
                        if (user.get("email") == username_text.text.toString()) {
                            if (user.get("EID") == password_text.text.toString()) {
                                (activity as NavigationHost).navigateTo(NavigationFragment(), false)
                            } else {
                                println("eid fail")
                            }
                        } else {
                            println("email fail")
                        }
                    }
                }
            }
        }
        return view
    }



    private fun fetchInfo(): String {
        val url = "https://comehither.appspot.com/usertable"

        val client = OkHttpClient()
        println("pls")
        val request = Request.Builder()
            .url(url)
            .header("User-Agent", "Android")
            .build()
        println("pls2")

        val response = client.newCall(request).execute()
        println("fuck me")
        val bodystr = response.body().string() // this can be consumed only once

        return bodystr
    }
}

