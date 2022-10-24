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

public class CustomAdapter2 extends BaseAdapter {

    Context context;
    ArrayList<itemModel2> arrayList;

    public CustomAdapter2(Context context, ArrayList<itemModel2> arrayList) {
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
        rating = (TextView) convertView.findViewById(R.id.rating);
        reviews = (TextView) convertView.findViewById(R.id.reviews);
        price = (TextView) convertView.findViewById(R.id.price);
        reviews_layout = (LinearLayout) convertView.findViewById(R.id.reviews_layout);
        rating_layout = (LinearLayout) convertView.findViewById(R.id.rating_layout);
        item_image = (ImageView) convertView.findViewById(R.id.item_image);



        site.setText(arrayList.get(position).getSite());

        title.setText(arrayList.get(position).getTitle());


        if(arrayList.get(position).getRating().equals("null")) {
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

        price.setText(arrayList.get(position).getPrice());

        Picasso.get()
                .load(arrayList.get(position).getImage())
                .placeholder(new ColorDrawable(0xFF808080))
//                .error(R.drawable.user_placeholder_error)
                .into(item_image);


        View.OnClickListener titleClick = new View.OnClickListener() {
            public void onClick(View v) {
                System.out.println("title");
                goToUrl(arrayList.get(position).getUrl());
            }
            private void goToUrl (String url) {
                Uri uriUrl = Uri.parse(url);
                Intent launchBrowser = new Intent(Intent.ACTION_VIEW, uriUrl);
                context.startActivity(launchBrowser);
            }
        };
        title.setOnClickListener(titleClick);

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
