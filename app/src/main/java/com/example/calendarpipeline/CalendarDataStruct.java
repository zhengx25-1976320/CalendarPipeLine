package com.example.calendarpipeline;

public class CalendarDataStruct {

    String eventTitle = "";
    Long startTime;
    Long endTime;
    //String description = "";
//    String location = "";

    public CalendarDataStruct(String eventTitle, Long startTime, Long endTime) { //String description,
        this.eventTitle = eventTitle;
        this.startTime = startTime;
        this.endTime = endTime;
        //this.description = description;
//        this.location = location;
    }

    @Override
    public String toString() {
        return "CalenderDataStruct{" +
                "eventTitle='" + eventTitle + '\'' +
                ", startTime='" + startTime + '\'' +
                ", endTime='" + endTime + '\'' +
                // ", description='" + description + '\'' +
//                ", location='" + location + '\'' +
                '}';
    }
}
