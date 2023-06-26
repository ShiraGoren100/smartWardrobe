package com.example.smartwardrobe.rate

import android.content.ContentValues.TAG
import android.os.Bundle
import android.util.Log
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.RadioButton
import androidx.lifecycle.lifecycleScope
import androidx.navigation.fragment.findNavController
import com.example.smartwardrobe.MainActivity
import com.example.smartwardrobe.RetrofitClient
import com.example.smartwardrobe.data.ClothingItem
import com.example.smartwardrobe.databinding.FragmentRateBinding
import com.google.android.material.snackbar.Snackbar
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.GlobalScope
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import okhttp3.ResponseBody
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response
import java.util.*

/**
 * A simple [Fragment] subclass as the default destination in the navigation.
 */
class RateFragment : Fragment() {

    private var _binding: FragmentRateBinding? = null

    // This property is only valid between onCreateView and
    // onDestroyView.
    private val binding get() = _binding!!

    /*private lateinit var ratingBar: RatingBar
    private lateinit var radioGroup: RadioGroup
    private lateinit var submitButton: Button*/
    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {

        _binding = FragmentRateBinding.inflate(inflater, container, false)
        return binding.root

    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        val today = Date().toString()
//        val id = (activity as RateActivity).receivedData
        binding.rateView.text = "Rate $today, /*$id*/ outfit"
        binding.submit.setOnClickListener {
//            val rating = binding.ratingBar.rating
            val selectedRadioButtonId = binding.radioGroup.checkedRadioButtonId
            val selectedRadioButton = view.findViewById<RadioButton>(selectedRadioButtonId)
            val option = selectedRadioButton?.text.toString()
            saveRate( option, 5)
            // TODO: Save the rating and selected option or perform desired action
            //call retrofit to save to server
            Snackbar.make(view, "Rating submitted: Option: $option", Snackbar.LENGTH_LONG).setAction("Action", null).show()
            activity?.finish()
        }
    }

    private fun saveRate( option: String, outfitID: Int) {
        var retrofit = RetrofitClient.myApi
        val queryParameters = mapOf("id" to (activity as RateActivity).userId, "outfitID" to outfitID.toString(), "option" to option)
        val call = retrofit.rateOutfit(queryParameters)
        call.enqueue(object : Callback<ResponseBody> {
            override fun onResponse(call: Call<ResponseBody>, response: Response<ResponseBody>) {
                // handle successful response
//                callback.onSuccess()
                Log.i(TAG, "onResponse: success")
            }

            override fun onFailure(call: Call<ResponseBody>, t: Throwable) {
                // handle error
//                callback.onError("Error message")
                Log.e(TAG, "onFailure: ", t.cause)
            }
        })

        /*

            lifecycleScope.launch(Dispatchers.IO) {
                try {
                    val response = retrofit.rateOutfit(queryParameters as Map<String, String>)
                    if (response.isSuccessful) {
                        val data = response.body()
                        // Do something with the data
                    } else {
                        // Handle error
                    }
                } catch (e: Exception) {

                }
            }
    */

    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}