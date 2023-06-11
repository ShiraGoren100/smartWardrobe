package com.example.smartwardrobe.rate

import android.os.Bundle
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
            val rating = binding.ratingBar.rating
            val selectedRadioButtonId = binding.radioGroup.checkedRadioButtonId
            val selectedRadioButton = view.findViewById<RadioButton>(selectedRadioButtonId)
            val option = selectedRadioButton?.text.toString()
            saveRate(rating, option, 5)
            // TODO: Save the rating and selected option or perform desired action
            //call retrofit to save to server
            Snackbar.make(view, "Rating submitted: $rating\nOption: $option", Snackbar.LENGTH_LONG).setAction("Action", null).show()
            activity?.finish()
        }
    }

    private fun saveRate(rating: Float, option: String, outfitID: Int) {
        var retrofit = RetrofitClient.myApi
        val queryParameters = mapOf("id" to (activity as RateActivity).userId, "outfitID" to outfitID, "rating" to rating, "option" to option)

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
        return
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}