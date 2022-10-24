package com.example.calendarpipeline;

import android.content.Context;
import android.content.Intent;
import android.graphics.drawable.ColorDrawable;
import android.net.Uri;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.TextView;

import com.squareup.picasso.Picasso;

import java.util.ArrayList;

//import com.squareup.picasso.Picasso;

public class CustomAdapter extends BaseAdapter{

    Context context;
    ArrayList<com.example.calendarpipeline.itemModel> arrayList;

    public CustomAdapter(Context context, ArrayList<com.example.calendarpipeline.itemModel> arrayList) {
        this.context = context;
        this.arrayList = arrayList;



    }

    @Override
    public int getCount() {
        return arrayList.size();
    }

    @Override
    public Object getItem(int position) {
        return arrayList.get(position);
    }

    @Override
    public long getItemId(int i) {
        return i;
    }

    @Override
    public View getView(final int position, View convertView, ViewGroup parent) {
        if (convertView ==  null) {
            convertView = LayoutInflater.from(context).inflate(R.layout.item_list_1, parent, false);
        }
        TextView site, title, url, rating, reviews, price, searchurl;
        LinearLayout reviews_layout, rating_layout;
        ImageView item_image;


        site = (TextView) convertView.findViewById(R.id.site);
        title = (TextView) convertView.findViewById(R.id.title);
//        url = (TextView) convertView.findViewById(R.id.url);
        rating = (TextView) convertView.findViewById(R.id.rating);
        reviews = (TextView) convertView.findViewById(R.id.reviews);
        price = (TextView) convertView.findViewById(R.id.price);
        reviews_layout = (LinearLayout) convertView.findViewById(R.id.reviews_layout);
        rating_layout = (LinearLayout) convertView.findViewById(R.id.rating_layout);
//        searchurl = (TextView) convertView.findViewById(R.id.searchurl);
        item_image = (ImageView) convertView.findViewById(R.id.item_image);



//        site.setText(arrayList.get(position).getSite());
        site.setText(arrayList.get(position).getSite());

        title.setText(arrayList.get(position).getTitle());

//        url.setText(arrayList.get(position).getUrl());

        if(arrayList.get(position).getRating().equals("null")) {
//            rating.setText("");
//            System.out.println(arrayList.get(position));
            rating_layout.setVisibility(View.GONE);
        } else {
            rating_layout.setVisibility(View.VISIBLE);
            rating.setText(arrayList.get(position).getRating());
        }

        if(arrayList.get(position).getReviews().equals("null")) {
            rating_layout.setVisibility(View.GONE);
        } else {
            rating_layout.setVisibility(View.VISIBLE);
            reviews.setText(arrayList.get(position).getReviews());
        }



//        reviews.setText(arrayList.get(position).getReviews());
        price.setText(arrayList.get(position).getPrice());
//        searchurl.setText(arrayList.get(position).getSearch_url());

//        item_image.setImageResource(arrayList.get(position).getImage());
//        System.out.println(arrayList.get(position).getImage());

//        if (arrayList.get(position).getImage().length() == 1) {
            Picasso.get()
//                .load("http://i.imgur.com/DvpvklR.png")
//                .load("https://m.media-amazon.com/images/I/71cP6IUwA1L._AC_UL320_.jpg")
//                .resize(81, 75)
                    .load(arrayList.get(position).getImage())
                    .placeholder(new ColorDrawable(0xFF808080))
//                .error(R.drawable.user_placeholder_error)
                    .into(item_image);
//        }


        View.OnClickListener titleClick = new View.OnClickListener() {
            public void onClick(View v) {
                System.out.println("title");
//                System.out.println(arrayList.get(position).getUrl());
                goToUrl(arrayList.get(position).getUrl());
            }
            private void goToUrl (String url) {
                Uri uriUrl = Uri.parse(url);
                Intent launchBrowser = new Intent(Intent.ACTION_VIEW, uriUrl);
                context.startActivity(launchBrowser);
            }
        };
        title.setOnClickListener(titleClick);



//        reviews.setOnClickListener({new View.OnClickListener() {
//            public void onClickReview (View v){
//                System.out.println("review");
////                System.out.println(arrayList.get(position).getUrl());
//                goToUrl(arrayList.get(position).getReviewLink());
//            }
//
//            private void goToUrl (String url) {
//                Uri uriUrl = Uri.parse(url);
//                Intent launchBrowser = new Intent(Intent.ACTION_VIEW, uriUrl);
//                context.startActivity(launchBrowser);
//            }
//        });

        View.OnClickListener reviewClick = new View.OnClickListener() {
            public void onClick(View v) {
                System.out.println("review");
                goToUrl(arrayList.get(position).getReviewLink());

            }
            private void goToUrl (String url) {
                Uri uriUrl = Uri.parse(url);
                Intent launchBrowser = new Intent(Intent.ACTION_VIEW, uriUrl);
                context.startActivity(launchBrowser);
            }
        };
        reviews.setOnClickListener(reviewClick);



        return convertView;
    }









}
